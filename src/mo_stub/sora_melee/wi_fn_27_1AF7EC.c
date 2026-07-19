void* fn_27_1AF7EC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 295) idx -= 295;
    return (char*)p + idx * 4 + 12;
}
