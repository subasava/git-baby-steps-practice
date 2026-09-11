module.exports = function validateRequest(req, res, next) {
  if (!req.body || typeof req.body !== 'object') {
    return res.status(400).json({ message: 'Request body must be a JSON object.' });
  }

  return next();
};
