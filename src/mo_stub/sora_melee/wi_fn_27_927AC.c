void* fn_27_927AC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 500) idx -= 500;
    return (char*)p + idx * 8 + 12;
}
