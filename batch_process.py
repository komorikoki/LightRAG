import os
import asyncio
from lightrag import LightRAG
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import setup_logger
import shutil

setup_logger("lightrag", level="INFO")

BASE_WORKING_DIR = "./preprocessed_rag_storage_jp_v2" 
DATA_DIR = "./data/output_files"
OUTPUT_DIR_PREFIX = "./archive_rag_storage_jp_v2_part_"

async def initialize_rag(source_dir, working_dir):

    japanese_system_prompt = """
    あなたはAIアシスタントです。これから与えられるテキストから、エンティティ（実体）とリレーション（関係性）を抽出してください。
    【重要事項】
    - 全てのエンティティとリレーションは、必ず日本語で出力しなければなりません。
    - 英語の単語は絶対に使用しないでください。例えば、「Teacher」ではなく「先生」、「Protagonist」ではなく「主人公」と出力してください。
    - 出力する前に、すべての単語が日本語であることを再度確認してください。
    """
    print(f"Copying data from {source_dir} to {working_dir}...")
    shutil.copytree(source_dir, working_dir)

    rag = LightRAG(
        working_dir=working_dir,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
        llm_model_kwargs={"system_prompt": japanese_system_prompt}
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag

async def main():
    rag = None
    source_dir = BASE_WORKING_DIR
    for i in range(1, 4):
        target_dir = f"{OUTPUT_DIR_PREFIX}{i}"
        rag = await initialize_rag(source_dir, target_dir)
        for j in range(1, 10):
            k = (i+2)*10 + j
            filename = f"part_{k}.txt"
            filepath = os.path.join(DATA_DIR, filename)

            try:
                print(f"--- Processing: {filepath} ---")
                with open(filepath, "r", encoding="utf-8") as file:
                    text = file.read()

                await rag.ainsert(text)
                print(f"Successfully inserted: {filepath}")
            except FileNotFoundError:
                print(f"Warning: ファイルが見つかりませんでした。スキップします: {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
        source_dir = target_dir
        print(f"Finalizing storages for {target_dir}...")
        await rag.finalize_storages()
        print("Done.")
    


if __name__ == "__main__":
    asyncio.run(main())