import streamlit as st

st.title("💰 我的智能记账本")

# --- 1. 记忆初始化 (解决金鱼记忆问题) ---
# 这句话的意思是：如果保险箱(session_state)里还没有 'my_bill_book'，那就新建一个空列表
if 'my_bill_book' not in st.session_state:
    st.session_state.my_bill_book = []

# --- 2. 侧边栏：输入区 ---
# st.sidebar 会把东西放在左边的侧边栏，看起来更像正经APP
st.sidebar.header("📝 记一笔")
item_name = st.sidebar.text_input("买了什么商品？")
# number_input 专门用来输数字，step=1 表示每次加减1
item_price = st.sidebar.number_input("花了多少钱？", min_value=0.0, step=1.0)

# --- 3. 按钮逻辑 ---
if st.sidebar.button("确认记账"):
    if item_name == "":
        st.sidebar.error("商品名不能为空哦！")
    else:
        # 生成一笔账单（字典）
        new_bill = {"item": item_name, "price": item_price}
        
        # 装进保险箱里的列表！注意这里是 st.session_state.my_bill_book
        st.session_state.my_bill_book.append(new_bill)
        
        st.sidebar.success(f"已添加：{item_name}")
if st.sidebar.button("清空账单"):
    st.session_state.my_bill_book = []
    st.sidebar.warning("账单已清空！")
    
# --- 4. 主界面：展示账单 ---
st.header("📋 账单明细")

# 如果列表是空的，提示一下
if len(st.session_state.my_bill_book) == 0:
    st.write("还没有记账，快去左边记一笔吧！")
else:
    # 遍历打印每一笔账（这是你熟悉的 for 循环）
    for bill in st.session_state.my_bill_book:
        # st.info 可以显示一个漂亮的蓝色条条
        st.info(f"商品: {bill['item']}   |   价格: {bill['price']} 元")

    # --- 5. 算总账 ---
    st.markdown("---") # 画一条分割线
    
    # 算出总金额
    total = 0
    for bill in st.session_state.my_bill_book:
        total = total + bill['price']
        
    # metric 是专门用来展示关键指标的大数字组件
    st.metric("总消费金额", f"{total} 元")