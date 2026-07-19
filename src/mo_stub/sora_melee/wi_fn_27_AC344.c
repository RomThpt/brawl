void* fn_27_AC344(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 25) idx -= 25;
    return (char*)p + idx * 4 + 12;
}
