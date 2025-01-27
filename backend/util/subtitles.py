def format_srt(srt: bytes) -> str:
    srt_txt = srt.decode("utf-8")
    blocks = srt_txt.split("\n\n")

    output = []
    for block in blocks:
        lines = block.split("\n")
        start_time, end_time = lines[1].split(" --> ")
        output.append(f"{start_time[:-4]}: {'\n'.join(lines[2:])}")
    return "\n\n".join(output)
