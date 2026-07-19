void* fn_27_268A78(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 8) idx -= 8;
    return (char*)p + idx * 24 + 12;
}
