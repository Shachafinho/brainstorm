// === Functions ===

function getUsersUrl(baseUrl) {
  return baseUrl + '/users';
}

function getUserUrl(baseUrl, userId) {
  return getUsersUrl(baseUrl) + '/' + userId.toString();
}

function getSnapshotsUrl(baseUrl, userId) {
  return getUserUrl(baseUrl, userId) + '/snapshots';
}

function getSnapshotUrl(baseUrl, userId, snapshotId) {
  return getSnapshotsUrl(baseUrl, userId) + '/' + snapshotId.toString();
}

function getResultUrl(baseUrl, userId, snapshotId, resultName) {
  return getSnapshotUrl(baseUrl, userId, snapshotId) + '/' + resultName;
}

// === Exports ===

export {
  getUsersUrl,
  getUserUrl,
  getSnapshotsUrl,
  getSnapshotUrl,
  getResultUrl,
};
