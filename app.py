import streamlit as st
import pandas as pd
import database
import matplotlib.pyplot as plt
#====================================
# TITLE
#====================================
st.title("DANYA Candle Dashboard")

#====================================
# ADD PRODUCT
#====================================
st.write("## Add Product")
candle_name = st.text_input("Candle Name")

sale_price = st.number_input(
    "Sale Price",
    min_value=0
)

cost_price = st.number_input(
    "Production Cost",
    min_value=0
)

stock = st.number_input(
    "Stock Quantity",
    min_value=0,
    step=1
)

if st.button("Add Product"):
    database.add_product(
        candle_name,
        sale_price,
        cost_price,
        stock
    )

    st.success("Product added successfully!")

#====================================
# LOAD PRODUCT
#====================================
products = database.get_products()

df = pd.DataFrame(
    products,
    columns=[
        "ID",
        "Candle Name",
        "Sale Price",
        "Cost Price",
        "Stock"
    ]
)

df["Profit"] = df["Sale Price"] - df["Cost Price"]

#====================================
# METRICS
#====================================
total_products = len(df)
total_inventory = df["Stock"].sum()
total_profit = (df["Profit"] * df["Stock"]).sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Products",
        total_products
    )

with col2:
    st.metric(
        "Inventory",
        total_inventory
    )

with col3:
    st.metric(
        "Potential Profit (T)",
        f"{total_profit:,.0f} T"
    )

#====================================
# TABLE
#====================================
st.write("## Product List")
st.dataframe(df)

#====================================
# DELETE PRODUCT
#====================================
st.write("## Delete Product")

product_id = st.number_input(
    "Enter Product ID",
    min_value=1,
    step=1
)

if st.button("Delete Product"):
    database.delete_product(product_id)
    st.success("Product deleted successfully!")

#====================================
# UPDATE PRODUCT
#====================================
st.write("## Update Product")

update_id = st.number_input(
    "Product ID",
    min_value=1,
    step=1,
    key="update_id"
)

new_sale_price = st.number_input(
    "New Sale Price",
    min_value=0,
    key="sale"
)

new_cost_price = st.number_input(
    "New Cost Price",
    min_value=0,
    key="cost"
)

new_stock = st.number_input(
    "New Stock",
    min_value=0,
    step=1,
    key="stock_update"
)

if st.button("Update Product"):
    database.update_product(
        update_id,
        new_sale_price,
        new_cost_price,
        new_stock
    )

    st.success("Product updated successfully!")

#====================================
# RECORD SALE
#====================================
st.write("## Record Sale")


sale_product_id = st.number_input(

    "Product ID",

    min_value=1,

    step=1,

    key="sale_id"

)

sale_quantity = st.number_input(

    "Quantity Sold",

    min_value=1,

    step=1,

    key="sale_quantity"

)

sale_date = st.date_input("Sale Date")

if st.button("Record Sale"):
    database.add_sale(
        sale_product_id,
        sale_quantity,
        str(sale_date)
    )

    database.decrease_stock(
        sale_product_id,
        sale_quantity
    )

    st.success("Sale recorded and stock updated!")
#====================================
# SALE HISTORY
#====================================
st.write("## Sales History")

sales = database.get_sales()

sales_df = pd.DataFrame(
    sales,
    columns=[
        "Sale ID",
        "Product ID",
        "Quantity",
        "Sale Date"
    ]
)

st.dataframe(sales_df)

# -------------------------
# REVENUE DASHBOARD
# -------------------------

st.write("## Revenue Dashboard")

sales_data = database.get_sales_details()

revenue = 0
cost = 0
units_sold = 0

for sale in sales_data:
    sale_price = sale[1]
    cost_price = sale[2]
    quantity = sale[3]

    revenue += sale_price * quantity
    cost += cost_price * quantity
    units_sold += quantity

profit = revenue - cost

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Revenue",
        f"{revenue:,.0f}"
    )

with col2:
    st.metric(
        "Cost",
        f"{cost:,.0f}"
    )

with col3:
    st.metric(
        "Profit",
        f"{profit:,.0f}"
    )

with col4:
    st.metric(
        "Units Sold",
        units_sold
    )
# -------------------------
# BEST SELLER
# -------------------------

st.write("## Best Seller")

best_seller = database.get_best_seller()

if best_seller:
    st.success(
        f"🏆 {best_seller[0]} ({best_seller[1]} sold)"
    )
else:
    st.info("No sales recorded yet.")

# -------------------------
# LOW STOCK ALERT
# -------------------------

st.write("## Low Stock Alert")

low_stock_products = df[df["Stock"] <= 3]

if len(low_stock_products) > 0:
    st.warning("Some products are running low!")

    st.dataframe(
        low_stock_products[
            [
                "ID",
                "Candle Name",
                "Stock"
            ]
        ]
    )

else:
    st.success(
        "All products have sufficient stock."
    )
# -------------------------
# SALES CHART
# -------------------------

st.write("## Sales Chart")

chart_data = database.get_sales_chart_data()

if chart_data:

    names = []
    quantities = []

    for item in chart_data:
        names.append(item[0])
        quantities.append(item[1])

    names = [name.split(" Candle")[0] for name in names]    

    fig, ax = plt.subplots(figsize=(8,4))

    ax.bar(
        names,
        quantities
    )

    ax.set_title("Products Sales")

    ax.set_ylabel("Units Sold")
    plt.xticks(rotation=45)
    st.pyplot(fig)