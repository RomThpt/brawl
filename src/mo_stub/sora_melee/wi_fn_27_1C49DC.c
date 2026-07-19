void* fn_27_1C49DC(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 28) + i;
    if (idx >= 5) idx -= 5;
    return (char*)p + idx * 12 + 28;
}
