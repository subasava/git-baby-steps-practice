function getRequestId() {
  return Math.random().toString(36).slice(2, 11);
}

module.exports = {
  getRequestId,
};
