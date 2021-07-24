##Discovery
[task file](files/6eb79e92b1c4e9e8f85b70f497d7c1b93342487243ca8c8161a9061b2207c6c57006b6e02c9890523dd8ab68beb737b18f8961ca2869367f0dd502b29d5f7c1c.zip)

When unpack file we can see 10 disk images, lets check what we have with file
```text
$file disk*     
disk01.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk02.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk03.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk04.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk05.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk06.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk07.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk08.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk09.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
disk10.img: Linux Software RAID version 1.2 (1) UUID=ad89154a:f0c39ce3:99c46240:21b5e681 name=0 level=5 disks=10
```
When we dont have mdadm installed we can see other output but google said thai is linux array

Lets examine them with mdadm util 
```text
$ mdadm --examine disk*
disk01.img:
          Magic : a92b4efc
        Version : 1.2
    Feature Map : 0x0
     Array UUID : ad89154a:f0c39ce3:99c46240:21b5e681
           Name : 0
  Creation Time : Wed Apr 28 01:39:00 2021
     Raid Level : raid5
   Raid Devices : 10

 Avail Dev Size : 8192
     Array Size : 36864 (36.00 MiB 37.75 MB)
    Data Offset : 2048 sectors
   Super Offset : 8 sectors
   Unused Space : before=1968 sectors, after=0 sectors
          State : clean
    Device UUID : c0e88e3c:62aaf6ff:d701e002:d4be4142

    Update Time : Wed Apr 28 03:11:16 2021
  Bad Block Log : 512 entries available at offset 16 sectors
       Checksum : badc0de - expected dbf6b2c8
         Events : 18

         Layout : left-symmetric
     Chunk Size : 4K

   Device Role : spare
   Array State : AAAAAAAAAA ('A' == active, '.' == missing, 'R' == replacing)
disk02.img:
          Magic : a92b4efc
        Version : 1.2
    Feature Map : 0x0
     Array UUID : ad89154a:f0c39ce3:99c46240:21b5e681
           Name : 0
  Creation Time : Wed Apr 28 01:39:00 2021
     Raid Level : raid5
   Raid Devices : 10

 Avail Dev Size : 8192
     Array Size : 36864 (36.00 MiB 37.75 MB)
    Data Offset : 2048 sectors
   Super Offset : 8 sectors
   Unused Space : before=1968 sectors, after=0 sectors
          State : clean
    Device UUID : 06ae0536:03b58132:72a9bd04:f473ba78

    Update Time : Wed Apr 28 03:11:16 2021
  Bad Block Log : 512 entries available at offset 16 sectors
       Checksum : badc0de - expected 404edf6a
         Events : 18

         Layout : left-symmetric
     Chunk Size : 4K

   Device Role : spare
   Array State : AAAAAAAAAA ('A' == active, '.' == missing, 'R' == replacing)
<output stripped>
```
Let also check superblock with hex editor(you can find superblock specification here [RAID_superblock_formats](https://raid.wiki.kernel.org/index.php/RAID_superblock_formats))

We can see that we don't have disk order in that array and some part of superblock is modified, so we can try to fix superblock (modify checksum and disk position) but it will take much more time. 

We can assemble that raid manually using the same configuration options and specific disk order

Let see what we have on disks to check what could help us to determine disk order we can see file

looking through content of disk we can see a lot of plain text which is a content of text file lets check if we have any file names with .txt

hooray we found file name shaks12.txt and text below
```text
shaks12.txt or shaks12.zip
```
so we can try to find original text, google a bit and found original text [shaks12.txt](files/shaks12.txt)

Text is very long and we can be shure that it will be present on each disk due to small chunk size

The simpliest way is find place when chunk with text has binary chunk after it

![text chunk and binary chunk](files/Screenshot%202021-07-24%20at%2004.38.09.png)
lets find text in original file
```text
Live, and be prosperous
```
original text is
```text
Live, and be prosperous; and farewell, good fellow.
  Bal. [aside] For all this same, I'll hide me hereabout.
```
so let's find second part
```text
$ grep "For all this same" disk*                                                                                                                                                                         1 ⨯
grep: disk07.img: binary file matches
```
so that we can decide that disk07.img is placed after disk01.img, so doing the same thing with disk07 we can found that next disk is disk04.img and the full sequence is 
```text
01->07->04->06->03->05->02->08->09->10 
``` 
let's create raid but before we can create loop device for each disk because mdadm can't work with images
```text
$ for i in {1..9}; do sudo losetup /dev/loop$i disk0$i.img; done
$ sudo losetup /dev/loop10 disk10.img
$ sudo mdadm --create --assume-clean --level=5 --raid-devices=10 --chunk=4  /dev/md0 /dev/loop1 /dev/loop7 /dev/loop4 /dev/loop6 /dev/loop3 /dev/loop5 /dev/loop2 /dev/loop8 /dev/loop9 /dev/loop10
mdadm: /dev/loop1 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop7 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop4 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop6 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop3 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop5 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop2 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop8 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop9 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
mdadm: /dev/loop10 appears to be part of a raid array:
       level=raid5 devices=10 ctime=Wed Apr 28 01:39:00 2021
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
```
Check array status
```text
$ cat /proc/mdstat 
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md0 : active raid5 loop10[9] loop9[8] loop8[7] loop2[6] loop5[5] loop3[4] loop6[3] loop4[2] loop7[1] loop1[0]
      36864 blocks super 1.2 level 5, 4k chunk, algorithm 2 [10/10] [UUUUUUUUUU]

```
try to mount and see what we have on filesystem
```text
$ sudo mount /dev/md0 /mnt                                                                                                                                                                         
                                                                                                                                                                                                             
$ sudo ls /mnt
flag.jpg              not-the-flag-054.jpg  not-the-flag-109.jpg  not-the-flag-164.jpg  not-the-flag-219.jpg  not-the-flag-274.jpg  not-the-flag-329.jpg  not-the-flag-384.jpg  not-the-flag-439.jpg
lost+found            not-the-flag-055.jpg  not-the-flag-110.jpg  not-the-flag-165.jpg  not-the-flag-220.jpg  not-the-flag-275.jpg  not-the-flag-330.jpg  not-the-flag-385.jpg  not-the-flag-440.jpg
not-the-flag-001.jpg  not-the-flag-056.jpg  not-the-flag-111.jpg  not-the-flag-166.jpg  not-the-flag-221.jpg  not-the-flag-276.jpg  not-the-flag-331.jpg  not-the-flag-386.jpg  not-the-flag-441.jpg
not-the-flag-002.jpg  not-the-flag-057.jpg  not-the-flag-112.jpg  not-the-flag-167.jpg  not-the-flag-222.jpg  not-the-flag-277.jpg  not-the-flag-332.jpg  not-the-flag-387.jpg  not-the-flag-442.jpg
not-the-flag-003.jpg  not-the-flag-058.jpg  not-the-flag-113.jpg  not-the-flag-168.jpg  not-the-flag-223.jpg  not-the-flag-278.jpg  not-the-flag-333.jpg  not-the-flag-388.jpg  not-the-flag-443.jpg
not-the-flag-004.jpg  not-the-flag-059.jpg  not-the-flag-114.jpg  not-the-flag-169.jpg  not-the-flag-224.jpg  not-the-flag-279.jpg  not-the-flag-334.jpg  not-the-flag-389.jpg  not-the-flag-444.jpg
not-the-flag-005.jpg  not-the-flag-060.jpg  not-the-flag-115.jpg  not-the-flag-170.jpg  not-the-flag-225.jpg  not-the-flag-280.jpg  not-the-flag-335.jpg  not-the-flag-390.jpg  not-the-flag-445.jpg
not-the-flag-006.jpg  not-the-flag-061.jpg  not-the-flag-116.jpg  not-the-flag-171.jpg  not-the-flag-226.jpg  not-the-flag-281.jpg  not-the-flag-336.jpg  not-the-flag-391.jpg  not-the-flag-446.jpg
not-the-flag-007.jpg  not-the-flag-062.jpg  not-the-flag-117.jpg  not-the-flag-172.jpg  not-the-flag-227.jpg  not-the-flag-282.jpg  not-the-flag-337.jpg  not-the-flag-392.jpg  not-the-flag-447.jpg
not-the-flag-008.jpg  not-the-flag-063.jpg  not-the-flag-118.jpg  not-the-flag-173.jpg  not-the-flag-228.jpg  not-the-flag-283.jpg  not-the-flag-338.jpg  not-the-flag-393.jpg  not-the-flag-448.jpg
not-the-flag-009.jpg  not-the-flag-064.jpg  not-the-flag-119.jpg  not-the-flag-174.jpg  not-the-flag-229.jpg  not-the-flag-284.jpg  not-the-flag-339.jpg  not-the-flag-394.jpg  not-the-flag-449.jpg
not-the-flag-010.jpg  not-the-flag-065.jpg  not-the-flag-120.jpg  not-the-flag-175.jpg  not-the-flag-230.jpg  not-the-flag-285.jpg  not-the-flag-340.jpg  not-the-flag-395.jpg  not-the-flag-450.jpg
not-the-flag-011.jpg  not-the-flag-066.jpg  not-the-flag-121.jpg  not-the-flag-176.jpg  not-the-flag-231.jpg  not-the-flag-286.jpg  not-the-flag-341.jpg  not-the-flag-396.jpg  not-the-flag-451.jpg
not-the-flag-012.jpg  not-the-flag-067.jpg  not-the-flag-122.jpg  not-the-flag-177.jpg  not-the-flag-232.jpg  not-the-flag-287.jpg  not-the-flag-342.jpg  not-the-flag-397.jpg  not-the-flag-452.jpg
not-the-flag-013.jpg  not-the-flag-068.jpg  not-the-flag-123.jpg  not-the-flag-178.jpg  not-the-flag-233.jpg  not-the-flag-288.jpg  not-the-flag-343.jpg  not-the-flag-398.jpg  not-the-flag-453.jpg
not-the-flag-014.jpg  not-the-flag-069.jpg  not-the-flag-124.jpg  not-the-flag-179.jpg  not-the-flag-234.jpg  not-the-flag-289.jpg  not-the-flag-344.jpg  not-the-flag-399.jpg  not-the-flag-454.jpg
not-the-flag-015.jpg  not-the-flag-070.jpg  not-the-flag-125.jpg  not-the-flag-180.jpg  not-the-flag-235.jpg  not-the-flag-290.jpg  not-the-flag-345.jpg  not-the-flag-400.jpg  not-the-flag-455.jpg
not-the-flag-016.jpg  not-the-flag-071.jpg  not-the-flag-126.jpg  not-the-flag-181.jpg  not-the-flag-236.jpg  not-the-flag-291.jpg  not-the-flag-346.jpg  not-the-flag-401.jpg  not-the-flag-456.jpg
not-the-flag-017.jpg  not-the-flag-072.jpg  not-the-flag-127.jpg  not-the-flag-182.jpg  not-the-flag-237.jpg  not-the-flag-292.jpg  not-the-flag-347.jpg  not-the-flag-402.jpg  not-the-flag-457.jpg
not-the-flag-018.jpg  not-the-flag-073.jpg  not-the-flag-128.jpg  not-the-flag-183.jpg  not-the-flag-238.jpg  not-the-flag-293.jpg  not-the-flag-348.jpg  not-the-flag-403.jpg  not-the-flag-458.jpg
not-the-flag-019.jpg  not-the-flag-074.jpg  not-the-flag-129.jpg  not-the-flag-184.jpg  not-the-flag-239.jpg  not-the-flag-294.jpg  not-the-flag-349.jpg  not-the-flag-404.jpg  not-the-flag-459.jpg
not-the-flag-020.jpg  not-the-flag-075.jpg  not-the-flag-130.jpg  not-the-flag-185.jpg  not-the-flag-240.jpg  not-the-flag-295.jpg  not-the-flag-350.jpg  not-the-flag-405.jpg  not-the-flag-460.jpg
not-the-flag-021.jpg  not-the-flag-076.jpg  not-the-flag-131.jpg  not-the-flag-186.jpg  not-the-flag-241.jpg  not-the-flag-296.jpg  not-the-flag-351.jpg  not-the-flag-406.jpg  not-the-flag-461.jpg
not-the-flag-022.jpg  not-the-flag-077.jpg  not-the-flag-132.jpg  not-the-flag-187.jpg  not-the-flag-242.jpg  not-the-flag-297.jpg  not-the-flag-352.jpg  not-the-flag-407.jpg  not-the-flag-462.jpg
not-the-flag-023.jpg  not-the-flag-078.jpg  not-the-flag-133.jpg  not-the-flag-188.jpg  not-the-flag-243.jpg  not-the-flag-298.jpg  not-the-flag-353.jpg  not-the-flag-408.jpg  not-the-flag-463.jpg
not-the-flag-024.jpg  not-the-flag-079.jpg  not-the-flag-134.jpg  not-the-flag-189.jpg  not-the-flag-244.jpg  not-the-flag-299.jpg  not-the-flag-354.jpg  not-the-flag-409.jpg  not-the-flag-464.jpg
not-the-flag-025.jpg  not-the-flag-080.jpg  not-the-flag-135.jpg  not-the-flag-190.jpg  not-the-flag-245.jpg  not-the-flag-300.jpg  not-the-flag-355.jpg  not-the-flag-410.jpg  not-the-flag-465.jpg
not-the-flag-026.jpg  not-the-flag-081.jpg  not-the-flag-136.jpg  not-the-flag-191.jpg  not-the-flag-246.jpg  not-the-flag-301.jpg  not-the-flag-356.jpg  not-the-flag-411.jpg  not-the-flag-466.jpg
not-the-flag-027.jpg  not-the-flag-082.jpg  not-the-flag-137.jpg  not-the-flag-192.jpg  not-the-flag-247.jpg  not-the-flag-302.jpg  not-the-flag-357.jpg  not-the-flag-412.jpg  not-the-flag-467.jpg
not-the-flag-028.jpg  not-the-flag-083.jpg  not-the-flag-138.jpg  not-the-flag-193.jpg  not-the-flag-248.jpg  not-the-flag-303.jpg  not-the-flag-358.jpg  not-the-flag-413.jpg  not-the-flag-468.jpg
not-the-flag-029.jpg  not-the-flag-084.jpg  not-the-flag-139.jpg  not-the-flag-194.jpg  not-the-flag-249.jpg  not-the-flag-304.jpg  not-the-flag-359.jpg  not-the-flag-414.jpg  not-the-flag-469.jpg
not-the-flag-030.jpg  not-the-flag-085.jpg  not-the-flag-140.jpg  not-the-flag-195.jpg  not-the-flag-250.jpg  not-the-flag-305.jpg  not-the-flag-360.jpg  not-the-flag-415.jpg  not-the-flag-470.jpg
not-the-flag-031.jpg  not-the-flag-086.jpg  not-the-flag-141.jpg  not-the-flag-196.jpg  not-the-flag-251.jpg  not-the-flag-306.jpg  not-the-flag-361.jpg  not-the-flag-416.jpg  not-the-flag-471.jpg
not-the-flag-032.jpg  not-the-flag-087.jpg  not-the-flag-142.jpg  not-the-flag-197.jpg  not-the-flag-252.jpg  not-the-flag-307.jpg  not-the-flag-362.jpg  not-the-flag-417.jpg  not-the-flag-472.jpg
not-the-flag-033.jpg  not-the-flag-088.jpg  not-the-flag-143.jpg  not-the-flag-198.jpg  not-the-flag-253.jpg  not-the-flag-308.jpg  not-the-flag-363.jpg  not-the-flag-418.jpg  not-the-flag-473.jpg
not-the-flag-034.jpg  not-the-flag-089.jpg  not-the-flag-144.jpg  not-the-flag-199.jpg  not-the-flag-254.jpg  not-the-flag-309.jpg  not-the-flag-364.jpg  not-the-flag-419.jpg  not-the-flag-474.jpg
not-the-flag-035.jpg  not-the-flag-090.jpg  not-the-flag-145.jpg  not-the-flag-200.jpg  not-the-flag-255.jpg  not-the-flag-310.jpg  not-the-flag-365.jpg  not-the-flag-420.jpg  not-the-flag-475.jpg
not-the-flag-036.jpg  not-the-flag-091.jpg  not-the-flag-146.jpg  not-the-flag-201.jpg  not-the-flag-256.jpg  not-the-flag-311.jpg  not-the-flag-366.jpg  not-the-flag-421.jpg  not-the-flag-476.jpg
not-the-flag-037.jpg  not-the-flag-092.jpg  not-the-flag-147.jpg  not-the-flag-202.jpg  not-the-flag-257.jpg  not-the-flag-312.jpg  not-the-flag-367.jpg  not-the-flag-422.jpg  not-the-flag-477.jpg
not-the-flag-038.jpg  not-the-flag-093.jpg  not-the-flag-148.jpg  not-the-flag-203.jpg  not-the-flag-258.jpg  not-the-flag-313.jpg  not-the-flag-368.jpg  not-the-flag-423.jpg  not-the-flag-478.jpg
not-the-flag-039.jpg  not-the-flag-094.jpg  not-the-flag-149.jpg  not-the-flag-204.jpg  not-the-flag-259.jpg  not-the-flag-314.jpg  not-the-flag-369.jpg  not-the-flag-424.jpg  not-the-flag-479.jpg
not-the-flag-040.jpg  not-the-flag-095.jpg  not-the-flag-150.jpg  not-the-flag-205.jpg  not-the-flag-260.jpg  not-the-flag-315.jpg  not-the-flag-370.jpg  not-the-flag-425.jpg  not-the-flag-480.jpg
not-the-flag-041.jpg  not-the-flag-096.jpg  not-the-flag-151.jpg  not-the-flag-206.jpg  not-the-flag-261.jpg  not-the-flag-316.jpg  not-the-flag-371.jpg  not-the-flag-426.jpg  not-the-flag-481.jpg
not-the-flag-042.jpg  not-the-flag-097.jpg  not-the-flag-152.jpg  not-the-flag-207.jpg  not-the-flag-262.jpg  not-the-flag-317.jpg  not-the-flag-372.jpg  not-the-flag-427.jpg  not-the-flag-482.jpg
not-the-flag-043.jpg  not-the-flag-098.jpg  not-the-flag-153.jpg  not-the-flag-208.jpg  not-the-flag-263.jpg  not-the-flag-318.jpg  not-the-flag-373.jpg  not-the-flag-428.jpg  not-the-flag-483.jpg
not-the-flag-044.jpg  not-the-flag-099.jpg  not-the-flag-154.jpg  not-the-flag-209.jpg  not-the-flag-264.jpg  not-the-flag-319.jpg  not-the-flag-374.jpg  not-the-flag-429.jpg  not-the-flag-484.jpg
not-the-flag-045.jpg  not-the-flag-100.jpg  not-the-flag-155.jpg  not-the-flag-210.jpg  not-the-flag-265.jpg  not-the-flag-320.jpg  not-the-flag-375.jpg  not-the-flag-430.jpg  raven.txt
not-the-flag-046.jpg  not-the-flag-101.jpg  not-the-flag-156.jpg  not-the-flag-211.jpg  not-the-flag-266.jpg  not-the-flag-321.jpg  not-the-flag-376.jpg  not-the-flag-431.jpg  shaks12.txt
not-the-flag-047.jpg  not-the-flag-102.jpg  not-the-flag-157.jpg  not-the-flag-212.jpg  not-the-flag-267.jpg  not-the-flag-322.jpg  not-the-flag-377.jpg  not-the-flag-432.jpg
not-the-flag-048.jpg  not-the-flag-103.jpg  not-the-flag-158.jpg  not-the-flag-213.jpg  not-the-flag-268.jpg  not-the-flag-323.jpg  not-the-flag-378.jpg  not-the-flag-433.jpg
not-the-flag-049.jpg  not-the-flag-104.jpg  not-the-flag-159.jpg  not-the-flag-214.jpg  not-the-flag-269.jpg  not-the-flag-324.jpg  not-the-flag-379.jpg  not-the-flag-434.jpg
not-the-flag-050.jpg  not-the-flag-105.jpg  not-the-flag-160.jpg  not-the-flag-215.jpg  not-the-flag-270.jpg  not-the-flag-325.jpg  not-the-flag-380.jpg  not-the-flag-435.jpg
not-the-flag-051.jpg  not-the-flag-106.jpg  not-the-flag-161.jpg  not-the-flag-216.jpg  not-the-flag-271.jpg  not-the-flag-326.jpg  not-the-flag-381.jpg  not-the-flag-436.jpg
not-the-flag-052.jpg  not-the-flag-107.jpg  not-the-flag-162.jpg  not-the-flag-217.jpg  not-the-flag-272.jpg  not-the-flag-327.jpg  not-the-flag-382.jpg  not-the-flag-437.jpg
not-the-flag-053.jpg  not-the-flag-108.jpg  not-the-flag-163.jpg  not-the-flag-218.jpg  not-the-flag-273.jpg  not-the-flag-328.jpg  not-the-flag-383.jpg  not-the-flag-438.jpg

```
lets check flag.jpg and Voi la flag is CTF{I_g0t_Str1p3s}

![flag](files/Screenshot%202021-07-24%20at%2005.02.18.png)