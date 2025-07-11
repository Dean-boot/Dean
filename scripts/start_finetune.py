from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 上傳訓練資料
upload = client.files.create(
    file=open("data/your_dataset.jsonl", "rb"),
    purpose="fine-tune"
)
print("✅ 檔案上傳成功：", upload.id)

# 開始 fine-tune
job = client.fine_tuning.jobs.create(
    training_file=upload.id,
    model="gpt-3.5-turbo"
)
print("🚀 Fine-tune 啟動成功：", job.id)
