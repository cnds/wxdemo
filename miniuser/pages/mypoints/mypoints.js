// pages/mypoints/mypoints.js
const app = getApp()
var status = require('../../utils/error.js')

Page({

  data: {

  },

  onLoad: function (options) {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/points',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: function(res) {
        if (res.statusCode === 200) {
          that.setData({
            points: res.data.points
          })
        } else if (res.statusCode === 400) {
          status.stauts400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  },
})