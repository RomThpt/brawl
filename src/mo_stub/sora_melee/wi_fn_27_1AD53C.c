void* fn_27_1AD53C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 27) + i;
    if (idx >= 12) idx -= 12;
    return (char*)p + idx * 12 + 28;
}
