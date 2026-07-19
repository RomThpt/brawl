void* fn_27_1B00FC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 36) idx -= 36;
    return (char*)p + idx * 16 + 12;
}
