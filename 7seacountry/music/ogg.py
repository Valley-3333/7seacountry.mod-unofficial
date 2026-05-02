import os
from pathlib import Path
from pydub import AudioSegment

def convert_mp3_to_ogg(input_dir, output_dir=None, quality="5"):
    """
    input_dir内のすべてのmp3をoggに変換する。
    quality: "0" (低) 〜 "10" (高)。"5"で約160kbps相当。
    """
    input_path = Path(input_dir)
    # 出力先が指定されていない場合は、入力と同じ場所に 'converted_ogg' フォルダを作る
    output_path = Path(output_dir) if output_dir else input_path / "converted_ogg"
    output_path.mkdir(parents=True, exist_ok=True)

    # フォルダ内の全てのmp3ファイルを取得
    mp3_files = list(input_path.glob("*.mp3"))
    
    if not mp3_files:
        print("変換対象のMP3ファイルが見つかりませんでした。")
        return

    print(f"{len(mp3_files)}個のファイルを処理します...")

    for mp3_file in mp3_files:
        try:
            print(f"変換中: {mp3_file.name}")
            
            # 音声ファイルの読み込み
            audio = AudioSegment.from_mp3(str(mp3_file))
            
            # HoI4推奨設定: サンプリングレートを44100Hzに設定
            audio = audio.set_frame_rate(44100)
            
            # 出力ファイル名の設定
            target_file = output_path / (mp3_file.stem + ".ogg")
            
            # エクスポート (libvorbisを使用)
            audio.export(
                str(target_file),
                format="ogg",
                codec="libvorbis",
                parameters=["-q:a", quality]
            )
            
        except Exception as e:
            print(f"エラー発生 ({mp3_file.name}): {e}")

if __name__ == "__main__":
    # 実行例: スクリプトと同じ階層の 'music_raw' フォルダを処理
    # パスは適宜書き換えてください
    convert_mp3_to_ogg("./music_raw")
    print("すべての処理が完了しました。")