---
blog: true
date: 2009-01-01
title: Install Linux With Pen Drive
categories: [IT]
tags: [Linux, Boot, LOF]
draft: false
---

>__Note: I would recommend you use the [unetbootin][unetbootin] to make the Linux bootable USB drive, since it is more easier (GUI) and convinience (auto-download distribution CD, auto-make boot flags). The below process just reach the same target, helping you understand what happened during the `unetbootin` process.__

---
In the very beginning, I thought it was really difficult to install a
linux from a USB, since it requires GRUB, kinds of alternative CD
media, and a "special" cd boot vmlinuz and initrd.gz files. Finally I
realise the power of GRUB, and it could boot anything, event a ISO
file.

# The Media

You need a portable USB drive or pen drive, whose capacity is larger
than 1GB, and a computer with capability of boot sequence selection

Download the Linux distribution CD image.

# Partition it 

1. Identify the USB device

        # dmesg | grep /dev/

2. Use `fdisk` to format the partition
	
		# fdisk /dev/sdb (run it as root or sudo fdisk /dev/sdb)
		press "n" to create a new partition
		press "p" to create the primary partition
		press "1" to create the number 1 primary partion
		press "p" to view the current table, then you shall get the sdb1 now
		press "a", then "1" to toggle the sdb1 as bootable
		press "t", then "c" to change the system id as "windows 95"
		press "w", save all of the partition information to the USB drive

	
# Prepare the file system

Using the ISO file to install the Linux, you shall use a "FAT32" partition to
save the ISO file, otherwise the ISO couldn't be seeked by the GRUB loader

        # mkfs -t vfat /dev/sdb1 (replace sdb1 with your real media partition, do NOT be wrong)
    	# mount /dev/sdb1 /mnt
    	# cp ubuntu-11.04-desktop-i386.iso /mnt

or you can copy it from windows system, since the fat32 partition is working
under windows.

# Install the GRUB
GRUB is the bootloader, which will control how you start the OS, by ISO or by normal media

        # mount /dev/sdb1 /mnt
    	# grub-install --root-directory=/mnt /dev/sdb (replace sdb with your real USB drive id)

Now you got a bootable USB stick bearing the ubuntu installation media.

# Begin Linux Boot

1. Plugin your USB dirve and boot your system
2. Press "F12" and select boot from USB/Flash drive
3. then you will get a "grub>" prompt and stopped, that's what we wanna
4. Configure the boot parameter

        grub> ls

	you will get a list of partitions including your local hard disk partition and
	your USB partition. That's easily identified by the count of partition number,
	like (hd0,1)(hd1,1)(hd1,2),(hd1,3),etc. we only have 1 partition on USB, so
	(hd0,1) is the USB partition
    
        grub> set root='(hd0,1)'
        grub> loopback loop /ubuntu-11.04-desktop-i386.iso
        grub> linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=/ubuntu-11.04-desktop-i386.iso
        grub> initrd (loop)/casper/initrd.lz
		grub> boot

# Install the Linux
After you boot into the `live CD desktop`, you can use the `install to harddisk` function to install the Linux copy to your local HDD or another USB drive.

# Notes
1. `loop` device

    The loopback command will assign the "loop" as themedia file (iso)
	
	Use the "TAB" key to let the `GRUB` to "seek" the possible files
	
    E.g. initrd file here is the `initrd.lz` not `initrd.gz`, you can
    use `TAB` after you typing the `initrd.`. The GRUB will
    automatically seek the initrd.lz**
	
2. GRUB is so powerful to read ISO or file system right before system
   "booted"
3. Use `FAT32` file system bearing the ISO file
4. You can using your existing `grub.cfg` (live system) to add the
   installation menuentry.
5. Do NOT try to install a new system on the same USB drive where your
   iso is
6. More examples of boot entry
    
		cat <<EOF> /mnt/boot/grub/grub.cfg
		menuentry "Ubuntu Live 9.10 32bit" {
		loopback loop /boot/iso/ubuntu-9.10-desktop-i386.iso
		linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=/boot/iso/ubuntu-9.10-desktop-i386.iso noeject noprompt --
		initrd (loop)/casper/initrd.lz
		}

		menuentry "Ubuntu Live 9.10 64bit" {
		loopback loop /boot/iso/ubuntu-9.10-desktop-amd64.iso
		linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=/boot/iso/ubuntu-9.10-desktop-amd64.iso noeject noprompt --
		initrd (loop)/casper/initrd.lz
		}

		menuentry "Grml small 2009.10" {
		loopback loop /boot/iso/grml-small_2009.10.iso
		linux (loop)/boot/grmlsmall/linux26 findiso=/boot/iso/grml-small_2009.10.iso apm=power-off lang=us vga=791 boot=live nomce noeject noprompt --
		initrd (loop)/boot/grmlsmall/initrd.gz
		}

		menuentry "tinycore" {
		loopback loop /boot/iso/tinycore_2.3.1.iso
		linux (loop)/boot/bzImage --
		initrd (loop)/boot/tinycore.gz
		}

		menuentry "Netinstall 32 preseed" {
		loopback loop /boot/iso/mini.iso
		linux (loop)/linux auto url=http://www.panticz.de/pxe/preseed/preseed.seed locale=en_US console-setup/layoutcode=de netcfg/choose_interface=eth0 debconf/priority=critical --
		initrd (loop)/initrd.gz
		}

		menuentry "debian-installer-amd64.iso" {
		loopback loop /boot/iso/debian-installer-amd64.iso
		linux (loop)/linux vga=normal --
		initrd (loop)/initrd.gz
		}

		menuentry "BackTrack 4" {
		linux /boot/bt4/boot/vmlinuz BOOT=casper boot=casper nopersistent rw vga=0x317 --
		initrd /boot/bt4/boot/initrd.gz
		}

		menuentry "Memory test (memtest86+)" {
		linux16 /boot/img/memtest86+.bin
		}

		menuentry "BackTrack ERR" {
		loopback loop /boot/iso/bt4-pre-final.iso
		linux (loop)/boot/vmlinuz find_iso/filename=/boot/iso/bt4-pre-final.iso BOOT=casper boot=casper nopersistent rw vga=0x317--
		initrd (loop)/boot/initrd.gz
		}

		menuentry "XBMC ERR" {
		loopback loop /boot/iso/XBMCLive.iso
		linux (loop)/vmlinuz boot=cd isofrom=/dev/sda1/boot/iso/XBMCLive.iso xbmc=nvidia,nodiskmount,tempfs,setvolume loglevel=0 --
		initrd (loop)/initrd0.img
		}

		menuentry "netboot.me" {
		loopback loop /boot/iso/netbootme.iso
		linux16 (loop)/GPXE.KRN
		}

		menuentry "debian installer amd64 netboot XEN pressed" {
		linux /boot/debian/linux auto preseed/url=http://www.panticz.de/pxe/preseed/xen.seed locale=en_US console-setup/layoutcode=de netcfg/choose_interface=eth0 debconf/priority=critical --
		initrd /boot/debian/initrd.gz
		}
		EOF

---
[unetbootin]: http://unetbootin.sourceforge.net

Last Updated: Sep 06, 2013 23:10 Manil
