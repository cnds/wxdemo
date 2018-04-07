// pages/transactions/transactions.js
const app = getApp()
var status = require('../../utils/error.js')

Page({
  data: {
    orders: null
  },
  transactionClick: function(event) {
    // console.log(event)
  },
  onLoad: function(event) {
    var that = this
    // console.log(app.globalData)
    wx.request({
      url: app.globalData.config.gateway + '/stores/' + app.globalData.storeInfo.id + '/orders',
      header: {'Authorization': 'Bearer ' + app.globalData.storeInfo.token},
      success: function(res) {
        if (res.statusCode === 200) {
          var orders = res.data.orders
          for (var order of orders) {
            order['createdDate'] = new Date(order.createdDate).toLocaleString()
          }
          that.setData({
            orders: orders
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