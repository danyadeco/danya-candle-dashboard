import streamlit as st
import pandas as pd
import database

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