#include <gf/gf_file_io.h>

extern DVDDiskID s_diskId;

const DVDDiskID* gfFileIO::getDVDDiskId() {
    return &s_diskId;
}
