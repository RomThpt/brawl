void* fn_27_D9CC8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 44) idx -= 44;
    return (char*)p + idx * 24 + 12;
}
