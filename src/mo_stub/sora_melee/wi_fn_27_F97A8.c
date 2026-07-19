void* fn_27_F97A8(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 27) + i;
    if (idx >= 12) idx -= 12;
    return (char*)p + idx * 12 + 28;
}
