function myFunction() {
  let file = getLatestFile();
  if (file == null) {
    Logger.log("最新のファイルはS3に転送済み");
    return;
  }

  let fileName = file.getName();
  Logger.log(file);
  let blob = file.getBlob();
  let s3 = getInstance(AccessKeyId, SecretAccessKey);

  s3.putObject(BucketName, FileName, blob, {logRequests:true});

  // 同じファイルを繰り返しS3に転送しないようラベルを設定
  file.setName('[転送済み]' + fileName);
}

function getLatestFile() {
  const folderID = Folder ID of Google Drive;
  const folder = DriveApp.getFolderById(folderID);
  const files = folder.getFiles();

  let file;
  let date;
  let latestFile;
  let latestDate = new Date(0);
  while (files.hasNext()) {
    file = files.next();
    date = file.getLastUpdated();
    if (date > latestDate) {
      latestDate = date;
      latestFile = file;
    }
  }

  const latestFileName = latestFile.getName();
  if (latestFileName.search('[転送済み]') < 0) {
    return (latestFile);
  } else {
    return;
  }
}