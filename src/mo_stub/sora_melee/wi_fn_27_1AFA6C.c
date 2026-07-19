void* fn_27_1AFA6C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 29) + i;
    if (idx >= 3) idx -= 3;
    return (char*)p + idx * 4 + 12;
}
