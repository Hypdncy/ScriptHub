#!/usr/bin/env bash
# -*- coding:utf-8 -*-

cd /dbapp/cvs/cvs/ || exit
git pull

cd /dbapp/baseline/webui || exit
git pull
npm run build

cd /dbapp/baseline/baseline/ || exit
git pull

bash update.sh
