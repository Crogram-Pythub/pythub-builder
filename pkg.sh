#!/bin/bash

appName="PythubBuilder"
# MacDeveloperID="3rd Party Mac Developer Installer: Developer Name (XXXX)"
MacDeveloperID="Developer ID Installer: CROGRAM INC. (4LWSS9P873)"

# rm -rf ./build/pkg
mkdir ./build/pkg

appPath=./dist/"$appName".app
pkgPath=./dist/"$appName".pkg


# 生成中间 PKG 文件
pkgbuild --install-location /Applications --component "$appPath" ./build/pkg/intermediate.pkg

cd ./build/pkg

# 创建分发 XML 文件
productbuild --synthesize --package ./intermediate.pkg ./distribution.xml

# 生成最终的 PKG 文件。此 PKG 文件未签名
productbuild --distribution ./distribution.xml --package-path ./intermediate.pkg ./unsigned_final.pkg


if ["$MacDeveloperID" = ""]; then
    # 未签名
    mv ./unsigned_final.pkg ./final.pkg
else
    # 使用 Mac 开发人员 ID 证书对 PKG 文件进行签名
    productsign --sign "$MacDeveloperID" ./unsigned_final.pkg ./signed_final.pkg
    mv ./signed_final.pkg ./final.pkg
fi

cd -

# rm "$pkgPath"
mv ./build/pkg/final.pkg "$pkgPath"
