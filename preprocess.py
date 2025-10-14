import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, gpt_4o_complete, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import setup_logger

setup_logger("lightrag", level="INFO")

# 定数としてディレクトリパスを定義
WORKING_DIR = "./preprocessed_rag_storage"
DATA_DIR = "./data/output_files"

# --- この関数は変更ありません ---
async def initialize_rag():
    """LightRAGインスタンスを初期化する"""
    if not os.path.exists(WORKING_DIR):
        os.mkdir(WORKING_DIR)

    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        # llm_model_func=gpt_4o_mini_complete,
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag

async def main():
    rag = None
    try:
        # LightRAGインスタンスを一度だけ初期化
        rag = await initialize_rag()

        # part_1.txt から part_30.txt までをループで処理
        for i in range(1, 31):
            filename = f"part_{i}.txt"
            filepath = os.path.join(DATA_DIR, filename)

            try:
                print(f"--- Processing: {filepath} ---")
                with open(filepath, "r", encoding="utf-8") as file:
                    text = file.read()
                
                # ファイルの内容をグラフに非同期で挿入
                await rag.ainsert(text)
                print(f"Successfully inserted: {filepath}")

            except FileNotFoundError:
                print(f"Warning: ファイルが見つかりませんでした。スキップします: {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
        
        print("\nすべてのファイルの処理が完了しました。")
        # results = await rag.aquery("物語の主題は何ですか？")
        # print(results)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # ループ処理がすべて終わった後に、一度だけストレージをファイナライズ
        if rag:
            print("Finalizing storages...")
            await rag.finalize_storages()
            print("Done.")

if __name__ == "__main__":
    asyncio.run(main())