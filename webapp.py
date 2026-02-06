import streamlit as st
from supabase import create_client, Client

# --- 1. 连接数据库 ---
# 从 Secrets 里读取钥匙
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("数据库连接失败！请检查 Secrets 配置。")
    st.stop()

st.title("💰 我的云端智能记账本")
st.caption("数据由 Supabase (PostgreSQL) 强力驱动")

# --- 2. 侧边栏：输入区 ---
st.sidebar.header("📝 记一笔")
item_name = st.sidebar.text_input("买了什么商品？")
item_price = st.sidebar.number_input("花了多少钱？", min_value=0.0, step=1.0)

if st.sidebar.button("确认记账"):
    if item_name == "":
        st.sidebar.error("商品名不能为空哦！")
    else:
        # 【关键代码】写入数据到 Supabase
        # table('bills') -> 找到表
        # insert(...) -> 插入字典数据
        # execute() -> 执行！
        try:
            data = {"item": item_name, "price": item_price}
            supabase.table("bills").insert(data).execute()
            st.sidebar.success(f"已上传：{item_name}")
            
            # 强制刷新页面，让新数据立刻显示出来
            st.rerun() 
            
        except Exception as e:
            st.sidebar.error(f"写入失败: {e}")

# --- 3. 主界面：展示账单 ---
st.header("📋 历史账单")

# 【关键代码】从 Supabase 读取数据
# select("*") 意思是选择所有列
# order("id", desc=True) 意思是按ID倒序排列（最新的在最上面）
response = supabase.table("bills").select("*").order("id", desc=True).execute()
bills_data = response.data # 获取真正的数据列表

if not bills_data:
    st.write("还没有记账，快去左边记一笔吧！")
else:
    # 算总账
    total = sum([item['price'] for item in bills_data])
    st.metric("历史总消费", f"{total} 元")

    # 展示每一行
    for bill in bills_data:
        # bill 现在是数据库里的一行数据
        # bill['created_at'] 是系统自动生成的时间，稍微有点长，我们截取前10位(日期)
        date_str = bill['created_at'][:10]
        st.info(f"{date_str} | 商品: {bill['item']} | 价格: {bill['price']} 元")

# --- 4. 清空功能 (慎用) ---
if st.sidebar.checkbox("开启管理员模式"):
    if st.sidebar.button("🗑️ 删库跑路 (清空所有)"):
        # delete().neq("id", 0) 这是一个黑客技巧
        # 意思是：删除所有 ID 不等于 0 的数据（也就是全删）
        supabase.table("bills").delete().neq("id", 0).execute()
        st.success("数据库已清空！")
        st.rerun()
