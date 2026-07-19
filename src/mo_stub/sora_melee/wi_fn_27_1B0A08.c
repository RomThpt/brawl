void* fn_27_1B0A08(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 288) idx -= 288;
    return (char*)p + idx * 4 + 12;
}
