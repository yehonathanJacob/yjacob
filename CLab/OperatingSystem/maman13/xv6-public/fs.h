// On-disk file system format.
// Name: Yehonathan Jacob
// ID: 316304740
// Date: 05/01/2020
// Description:
// Both the kernel and user programs use this header file.


#define ROOTINO 1  // root i-number
#define BSIZE 512  // block size

// Disk layout:
// [ boot block | super block | log | inode blocks |
//                                          free bit map | data blocks]
//
// mkfs computes the super block and builds an initial file system. The
// super block describes the disk layout:
struct superblock {
  uint size;         // Size of file system image (blocks)
  uint nblocks;      // Number of data blocks
  uint ninodes;      // Number of inodes.
  uint nlog;         // Number of log blocks
  uint logstart;     // Block number of first log block
  uint inodestart;   // Block number of first inode block
  uint bmapstart;    // Block number of first free map block
};

/*

  Add code that supports double indirection.

  Take a look on NDIRECT, NINDIRECT, MAXFILE, and the addrs[] element of struct dinode

  You'll have to have only 11 direct blocks, rather than 12, to make room for your new doubly-indirect block; you're not
  allowed to change the size of an on-disk inode. The first 11 elements of ip->addrs[] should be direct blocks; the 12th
  should be a singly-indirect block (just like the current one); the 13th should be your new doubly-indirect block.

*/
// 11 NDIRECT + 1 NINDIRECT + 1 doubly-indirect = 13
// Adding a block with NINDIRECT directions to bloaks that each one has NINDIRECT directions
#define NDIRECT 11
#define NINDIRECT (BSIZE / sizeof(uint))
#define MAXFILE (NDIRECT + NINDIRECT+ NINDIRECT*NINDIRECT)

// On-disk inode structure
struct dinode {
  short type;           // File type
  short major;          // Major device number (T_DEV only)
  short minor;          // Minor device number (T_DEV only)
  short nlink;          // Number of links to inode in file system
  uint size;            // Size of file (bytes)
  uint addrs[NDIRECT+2];   // Data block addresses
};

// Inodes per block.
#define IPB           (BSIZE / sizeof(struct dinode))

// Block containing inode i
#define IBLOCK(i, sb)     ((i) / IPB + sb.inodestart)

// Bitmap bits per block
#define BPB           (BSIZE*8)

// Block of free map containing bit for block b
#define BBLOCK(b, sb) (b/BPB + sb.bmapstart)

// Directory is a file containing a sequence of dirent structures.
#define DIRSIZ 14

struct dirent {
  ushort inum;
  char name[DIRSIZ];
};

