// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


chrome.runtime.onMessage.addListener(function(response,sender){
  var user_activity = {};
  
  user_activity['activity'] = response.activity;
  user_activity['count'] = 1;
  user_activity['usern'] = response.usern;
  //user_activity[response.activity] = user_activity[response.activity] + 1;
  //alert(user_activity[response.activity]);
  //var receiver = 'http://127.0.0.1:5000/user/'+String(response.usern);
  $.post('http://127.0.0.1:5000/profile',user_activity)
  console.log(user_activity);
});

