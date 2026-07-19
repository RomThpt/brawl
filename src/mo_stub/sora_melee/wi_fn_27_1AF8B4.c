void* fn_27_1AF8B4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 289) idx -= 289;
    return (char*)p + idx * 4 + 12;
}
