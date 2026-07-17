import itertools

FILE = "src/sora/ip/ip_network_producer.cpp"
OBJ = "build/RSBE01_02/src/sora/ip/ip_network_producer.o"
UNIT = "main/sora/ip/ip_network_producer"
SYMBOL = "networkInCallback__17ipNetworkProducerFPCUs"

ORIGINAL = """void ipNetworkProducer::networkInCallback(const u16* p1) {
    if (!g_ipNetworkProducer) {
        g_ipNetworkProducer = new (Heaps::SystemFW) ipNetworkProducer(true);
    }
    ipNetworkProducer* ip = g_ipNetworkProducer;
    u8* r7 = reinterpret_cast<u8*>(ip);
    u8 r6 = 0;
    if (ip->unk0) {
        r6 = r7[ip->unk0] + 1;
    }
    if (r6 >= 1) {
        r6 = 0;
    }

    r7[ip->unk0 + 1] = r6;
    UnkIpNetworkMsg* r5 = &ip->unk2 + r6;
    for (s32 i = 0; i < 8; i++) {
        r5->unk0[i] = p1[i];
    }

    ip->unk0++;
}"""

HEAD = """void ipNetworkProducer::networkInCallback(const u16* p1) {
    if (!g_ipNetworkProducer) {
        g_ipNetworkProducer = new (Heaps::SystemFW) ipNetworkProducer(true);
    }
    ipNetworkProducer* ip = g_ipNetworkProducer;"""

REST = """    if (ip->unk0) {
        r6 = r7[ip->unk0] + 1;
    }
    if (r6 >= 1) {
        r6 = 0;
    }

    r7[ip->unk0 + 1] = r6;
    UnkIpNetworkMsg* r5 = &ip->unk2 + r6;
    for (s32 i = 0; i < 8; i++) {
        r5->unk0[i] = p1[i];
    }

    ip->unk0++;
}"""

def decl(order, r6type, cast):
    castexpr = "reinterpret_cast<u8*>(ip)" if cast == "rc" else "(u8*)ip"
    dr7 = f"    u8* r7 = {castexpr};"
    dr6 = f"    {r6type} r6 = 0;"
    return (dr7 + "\n" + dr6) if order == "r7_r6" else (dr6 + "\n" + dr7)

CANDIDATES = []
seen = set()
for order in ["r7_r6", "r6_r7"]:
    for r6type in ["u8", "u32", "int", "s32"]:
        for cast in ["rc", "c"]:
            body = HEAD + "\n" + decl(order, r6type, cast) + "\n" + REST
            if body in seen:
                continue
            seen.add(body)
            CANDIDATES.append((f"{order}_{r6type}_{cast}", body))
