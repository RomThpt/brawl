void* fn_27_385B78(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 299) idx -= 299;
    return (char*)p + idx * 4 + 12;
}
