def get_checksum(header) -> str:
    checksum = 0
    overflow = 0

    for i in range(0, len(header), 2):
        word = header[i] + (header[i + 1] << 8)

        checksum = checksum + word
        overflow = checksum >> 16
        while overflow > 0:
            checksum = checksum & 0xFFFF
            checksum = checksum + overflow
            overflow = checksum >> 16
    overflow = checksum >> 16
    while overflow > 0:
        checksum = checksum & 0xFFFF
        checksum = checksum + overflow
        overflow = checksum >> 16

    checksum = ~checksum
    checksum = checksum & 0xFFFF

    return checksum