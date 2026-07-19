void* fn_27_2645E8(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 30) + i;
    if (idx >= 1) idx -= 1;
    return (char*)p + idx * 12 + 28;
}
