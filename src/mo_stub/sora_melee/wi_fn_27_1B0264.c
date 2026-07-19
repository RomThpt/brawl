void* fn_27_1B0264(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 15) idx -= 15;
    return (char*)p + idx * 16 + 12;
}
