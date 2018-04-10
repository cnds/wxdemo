// pages/transactions/transactions.js
const app = getApp()
var status = require('../../utils/error.js')

Page({

  data: {
    orders: null
  },

  onLoad: function (options) {
    this.getOrders()
  },

  getOrders: function () {
    var that = this
    wx.request({
      url: app.globalData.config.gateway + '/users/' + app.globalData.userId + '/orders',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: function(res) {
        if (res.statusCode === 200) {
          var orders = res.data.orders
          for (var order of orders) {
            var createdDate = new Date(order.createdDate)
            var day = createdDate.toLocaleDateString()
            var hour = createdDate.getHours().toString()
            if (hour.length === 1) {
              hour = '0' + hour
            }
            var minute = createdDate.getMinutes().toString()
            if (minute.length === 1) {
              minute = '0' + minute
            }
            order['createdDate'] = day + ' ' + hour + ':' + minute
          }
          that.setData({
            orders: res.data.orders
          })
        } else if (res.statusCode === 400) {
          status.status400(res.data.error)
        } else {
          status.status500()
        }
      }
    })
  }
})