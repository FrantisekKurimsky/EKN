"""Merit Order game page with visualization and Firebase storage."""
import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from datetime import datetime
from uuid import uuid4


def merit_order_page():
    """Interactive Merit Order game with capacity selection"""
    st.title("⚡ Merit Order")
    st.write("Nastavte si elektráreň, kapacitu, ponúkanú cenu a pozrite si, ako funguje trh.")

    # Load Excel data
    try:
        excel_file = "docs/merit_order_model.xlsx"
        wb = openpyxl.load_workbook(excel_file)
        assumptions_ws = wb["Assumptions"]

        # Extract technologies from Assumptions sheet
        technologies = {}
        for row_idx in range(6, 14):  # Rows 6-13 contain technology data
            tech_name = assumptions_ws[f"A{row_idx}"].value
            fuel_cost = assumptions_ws[f"B{row_idx}"].value
            efficiency = assumptions_ws[f"C{row_idx}"].value
            var_om = assumptions_ws[f"D{row_idx}"].value
            co2_intensity = assumptions_ws[f"E{row_idx}"].value
            capacity = assumptions_ws[f"G{row_idx}"].value

            if tech_name:
                technologies[tech_name.strip()] = {
                    "fuel_cost": fuel_cost,
                    "efficiency": efficiency if efficiency else 0,
                    "var_om": var_om,
                    "co2_intensity": co2_intensity if co2_intensity else 0,
                    "default_capacity": capacity if capacity else 0,
                }

    except Exception as e:
        st.error(f"Chyba pri načítaní Excelu: {e}")
        return

    st.subheader("📖 Ako to funguje")
    st.write("""
    1. **Vyberte technológiu** – jadro, plyn, uhlie, OZE...
    2. **Nastavte kapacitu** – koľko MW chcú vyrábať
    3. **Zadajte cenu** – za koľko EUR/MWh ponúkajú energiu
    4. **Nastavte demand** – koľko MW potrebuje trh
    5. **Výsledok** – graf ukáže poradie a vidíte, kto sa rozpredá
    """)

    # Initialize session state
    if "merit_order_bids" not in st.session_state:
        st.session_state.merit_order_bids = []
    if "merit_order_demand" not in st.session_state:
        st.session_state.merit_order_demand = 1500

    # Student input section
    st.markdown("---")
    st.subheader("⚙️ Pridaj elektráreň")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tech = st.selectbox("Technológia", list(technologies.keys()))
    with col2:
        default_cap = technologies[selected_tech]["default_capacity"]
        bid_capacity = st.number_input(
            "Kapacita (MW)", 
            min_value=10, 
            max_value=10000, 
            value=int(default_cap) if default_cap > 0 else 100,
            step=10
        )
    with col3:
        bid_price = st.number_input("Ponuka (EUR/MWh)", min_value=-100, max_value=500, value=50, step=5)

    if st.button("✅ Pridaj do merit order", use_container_width=True):
        st.session_state.merit_order_bids.append({
            "id": str(uuid4())[:8],
            "technology": selected_tech,
            "bid_price": bid_price,
            "capacity": bid_capacity,
            "added_at": datetime.utcnow().isoformat(),
        })
        st.success(f"✓ {selected_tech} ({bid_capacity} MW) pridaná s cenou {bid_price} EUR/MWh")

    # Demand slider
    st.markdown("---")
    st.subheader("📊 Nastavenie trhu")
    demand = st.number_input(
        "Dopyt (demand) – koľko MW potrebuje trh",
        min_value=100,
        max_value=10000,
        value=st.session_state.merit_order_demand,
        step=50,
    )
    st.session_state.merit_order_demand = demand

    # Visualization section
    st.markdown("---")
    st.subheader("📈 Analýza merit order")

    if not st.session_state.merit_order_bids:
        st.info("Zatiaľ neuvedené žiadne elektrárne. Pridajte aspoň jednu.")
    else:
        # Sort bids by price (merit order)
        sorted_bids = sorted(st.session_state.merit_order_bids, key=lambda x: x["bid_price"])

        # Calculate cumulative capacity for ALL bids
        cumulative_mw = 0
        cumulative_data = []
        
        for bid in sorted_bids:
            start_mw = cumulative_mw
            end_mw = cumulative_mw + bid["capacity"]
            cumulative_data.append({
                "technology": bid["technology"],
                "price": bid["bid_price"],
                "capacity": bid["capacity"],
                "cumulative_start": start_mw,
                "cumulative_end": end_mw,
                "dispatched": False,
            })
            cumulative_mw = end_mw

        # Now determine which are dispatched based on demand
        dispatch_list = []
        market_price = None
        
        for i, data in enumerate(cumulative_data):
            # Check if this plant is dispatched (demand is met)
            if data["cumulative_end"] <= demand:
                # Fully dispatched
                market_price = data["price"]
                dispatch_list.append(sorted_bids[i])  # Add the original bid object
            elif data["cumulative_start"] < demand < data["cumulative_end"]:
                # Partially dispatched
                market_price = data["price"]
                dispatch_list.append(sorted_bids[i])  # Add the original bid object
                break
            # If cumulative_start >= demand, not dispatched

        # Mark dispatched plants
        for data in cumulative_data:
                    data["dispatched"] = True

        # Define colors for each technology
        tech_colors = {
            "Nuclear": "#FFD700",           # Gold
            "Hydro": "#1E90FF",             # Dodger Blue
            "Wind": "#90EE90",              # Light Green
            "Solar": "#FF8C00",             # Dark Orange
            "Biomass": "#228B22",           # Forest Green
            "CCGT": "#FF6347",              # Tomato
            "OCGT": "#FF4500",              # Orange Red
            "Coal": "#2F4F4F",              # Dark Slate Gray
            "Oil": "#8B4513",               # Saddle Brown
        }

        # Create supply curve graph (filled steps)
        fig, ax = plt.subplots(figsize=(16, 8))

        # Plot filled steps for supply curve - ALL bids
        for i, data in enumerate(cumulative_data):
            color = tech_colors.get(data["technology"], "#CCCCCC")
            alpha = 1.0 if data["dispatched"] else 0.3  # Zapojené plne, nezapojené priehľadne
            
            # Fill area under this step
            ax.fill_between(
                [data["cumulative_start"], data["cumulative_end"]],
                0,
                data["price"],
                color=color,
                alpha=alpha,
                edgecolor="black",
                linewidth=1.5
            )
            
            # Draw the top line of this step
            ax.plot(
                [data["cumulative_start"], data["cumulative_end"]],
                [data["price"], data["price"]],
                color="black",
                linewidth=2
            )
            
            # Draw vertical connector to next step
            if i < len(cumulative_data) - 1:
                next_price = cumulative_data[i + 1]["price"]
                ax.plot(
                    [data["cumulative_end"], data["cumulative_end"]],
                    [data["price"], next_price],
                    color="black",
                    linewidth=2
                )

        # Add demand line
        if market_price is not None:
            ax.axvline(
                demand, 
                color="blue", 
                linestyle="--", 
                linewidth=2.5,
                alpha=0.8
            )
            ax.axhline(
                market_price, 
                color="red", 
                linestyle=":", 
                linewidth=2.5,
                alpha=0.8
            )

        # Labels and formatting
        ax.set_xlabel("Kumulovaná kapacita (MW)", fontsize=13, fontweight="bold")
        ax.set_ylabel("Cena (EUR/MWh)", fontsize=13, fontweight="bold")
        ax.set_title("⚡ Merit Order – Supply Curve", fontsize=15, fontweight="bold")
        ax.grid(axis="both", alpha=0.3, linestyle=":")
        
        # Set X limits to show ALL capacity
        if cumulative_data:
            max_cumulative = max(data["cumulative_end"] for data in cumulative_data)
            ax.set_xlim(0, max_cumulative * 1.1)
        else:
            ax.set_xlim(0, 100)
        
        # Set Y limits to show negative prices
        if cumulative_data:
            min_price = min(data["price"] for data in cumulative_data)
            max_price = max(data["price"] for data in cumulative_data)
            price_range = max_price - min_price
            ax.set_ylim(min_price - price_range * 0.15, max_price + price_range * 0.15)
        else:
            ax.set_ylim(-100, 100)
        
        # Add horizontal line at y=0 (break-even)
        ax.axhline(y=0, color="gray", linestyle="-", linewidth=0.8, alpha=0.5)

        st.pyplot(fig)

        # Market price and summary
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if market_price is not None:
                st.metric("🎯 Trhová cena", f"€{market_price}/MWh", delta=None)
            else:
                st.metric("🎯 Trhová cena", "—", delta="Nedostatok kapacity")

        with col2:
            total_capacity = sum(bid["capacity"] for bid in st.session_state.merit_order_bids)
            st.metric("📊 Celková kapacita", f"{total_capacity} MW")

        with col3:
            dispatched_mw = sum(bid["capacity"] for bid in dispatch_list)
            st.metric("⚡ Dispatch (zapojené)", f"{dispatched_mw} MW", delta=None)

        # Detailed dispatch table
        st.subheader("📋 Detail poradia")
        dispatch_df = pd.DataFrame([
            {
                "Poradie": i + 1,
                "Technológia": bid["technology"],
                "Ponuka (€/MWh)": bid["bid_price"],
                "Kapacita (MW)": bid["capacity"],
                "Status": "✓ Zapojená" if bid in dispatch_list else "✗ Nezapojená",
            }
            for i, bid in enumerate(sorted_bids)
        ])
        st.dataframe(dispatch_df, use_container_width=True, hide_index=True)

        # Revenue calculation
        if market_price is not None:
            st.subheader("💰 Výnosové tržby")
            revenue_data = []
            for bid in sorted_bids:
                revenue = bid["capacity"] * market_price if bid in dispatch_list else 0
                revenue_data.append({
                    "Technológia": bid["technology"],
                    "Kapacita (MW)": bid["capacity"],
                    "Cena (€/MWh)": market_price,
                    "Tržba (€)": f"{revenue:,.0f}",
                    "Status": "✓ Zapojená" if bid in dispatch_list else "✗ Nezapojená",
                })
            revenue_df = pd.DataFrame(revenue_data)
            st.dataframe(revenue_df, use_container_width=True, hide_index=True)

    # Management buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Vyčisti merit order", use_container_width=True):
            st.session_state.merit_order_bids = []
            st.rerun()
    with col2:
        if st.button("🔄 Zresetuj demand", use_container_width=True):
            st.session_state.merit_order_demand = 1500
            st.rerun()
