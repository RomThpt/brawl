void* fn_27_2949A8(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 30) idx -= 30;
    return (char*)p + idx * 12 + 28;
}
