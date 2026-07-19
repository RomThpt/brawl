void* fn_27_1B019C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 8) idx -= 8;
    return (char*)p + idx * 16 + 12;
}
