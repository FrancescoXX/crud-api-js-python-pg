const User = require('../models/users');

//Crud controllers

// Create one user
exports.createOne = async (req, res, next) => {
  console.log("createOne");
  try {
    const USER_MODEL = {
      username: req.body.username,
      email: req.body.email,
      password: req.body.password,
    }

    try {
      const user = await User.create(USER_MODEL);
      return res.status(201).json(user);
    } catch (error) {
      return res.status(500).json(error)
    }

  } catch (error) {
    return res.status(400).json("BAD Request", error);
  }
}

// GET ALL
exports.getAll = async (req, res, next) => {
  try {
    const ALL = await User.findAll();
    return res.status(200).json(ALL)
  } catch (error) {
    return res.status(500).json(error);
  }
}

// Get one User
exports.getOne = async (req, res, next) => {
  try {
    const user = await User.findByPk(req.params.id);
    return res.status(200).json(user)
  } catch (error) {
    return res.status(500).json("Error in getOne", error)
  }
}

//Update User
exports.updateOne = async (req, res, next) => {
  try {
    const USER_MODEL = {
      username: req.body.username,
      email: req.body.email,
      password: req.body.password,
    }

    try {
      const u = await User.update(USER_MODEL,{where: {id: req.params.id}})
      return res.status(200).json(u);
    } catch (error) {
      return res.status(500).json(error);
    }

  } catch (error) {
    return res.status(400).json(error);
  }
}

//Delete User
exports.deleteOne = async (req, res, next) => {
  try {
    const user = await User.destroy({ where: { id: req.params.id } });
    return res.status(200).json("the user has been deleted! Id: ", req.params.id);
  } catch (error) {
    return res.status(500).json("Error in deleteOne", error)
  }
}