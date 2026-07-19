void* fn_27_1B1410(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 10) idx -= 10;
    return (char*)p + idx * 20 + 12;
}
