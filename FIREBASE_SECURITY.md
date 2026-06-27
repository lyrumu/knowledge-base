# Firebase 安全配置说明

> 适用项目：`f:\Notes`
> 用途：给 Blowfish 原生 `views / likes` 提供数据来源，同时尽量把风险收紧到最小。

---

## 1. 先知道一件事

- `apiKey`、`authDomain`、`projectId` 这类 Firebase Web 配置**会暴露在前端**
- 这是正常的，不是泄漏事故
- 真正决定安不安全的，是：
  - `Firestore Security Rules`
  - `Authentication` 的允许方式
  - 你是否只开放了最小必要权限

---

## 2. 本项目推荐的最小安全方案

只做这两件事：

1. 开启 `Anonymous Authentication`
2. 给 `Firestore` 配一套只允许 `views / likes` 以受控方式变化的规则

不要做的事：

- 不要为了图省事把 Firestore 改成“测试模式长期开放”
- 不要允许任意 collection 任意读写
- 不要在规则里给未认证用户开放无限制写权限

---

## 3. Authentication 要怎么开

Firebase 控制台：

1. 打开 `Build > Authentication`
2. 点击 `Get started`
3. 打开 `Sign-in method`
4. 启用 `Anonymous`
5. 保存

原因：

- Blowfish 的 Firebase 脚本默认会在前端执行 `signInAnonymously`
- 如果你不开匿名登录：
  - `views` 不会正常累计
  - `likes` 也不会正常工作

---

## 4. Firestore Rules 推荐直接用这个

Firebase 控制台：

1. 打开 `Build > Firestore Database`
2. 进入 `Rules`
3. 用下面这份规则覆盖并发布

```txt
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Views - authenticated users can read; writes are tightly limited
    match /views/{document} {
      allow read: if request.auth != null;
      allow create: if request.auth != null
                    && request.resource.data.keys().hasOnly(['views'])
                    && request.resource.data.views == 1;
      allow update: if request.auth != null
                    && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['views'])
                    && request.resource.data.views == resource.data.views + 1;
    }

    // Likes - authenticated users can read; value can only go +1 / -1 and never below 0
    match /likes/{document} {
      allow read: if request.auth != null;
      allow create: if request.auth != null
                    && request.resource.data.keys().hasOnly(['likes'])
                    && request.resource.data.likes == 1;
      allow update: if request.auth != null
                    && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['likes'])
                    && (request.resource.data.likes == resource.data.likes + 1
                        || request.resource.data.likes == resource.data.likes - 1)
                    && request.resource.data.likes >= 0;
    }

    // Deny everything else
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

这份规则的含义：

- `views`
  - 只能创建为 `1`
  - 后续每次只能 `+1`
- `likes`
  - 只能创建为 `1`
  - 后续只能 `+1` 或 `-1`
  - 不允许变成负数
- 除了 `views/*` 和 `likes/*`
  - 其他任何文档都不允许读写

---

## 5. 这套规则能防什么

- 防止有人随便往你的 Firestore 里写乱七八糟的字段
- 防止把某篇文章的 `views` 一次性改成 `999999`
- 防止把 `likes` 改成负数
- 防止借你的 Firebase 项目当通用数据库乱写其他 collection

---

## 6. 这套规则不能防什么

- 不能彻底防止“有人反复刷新 / 换浏览器 / 换设备”带来的轻度刷量
- 不能做到真正的账号级防刷
- 不能做到复杂风控

为什么：

- Blowfish 的原生实现是轻量方案
- 它依赖：
  - 匿名登录
  - 本地 `localStorage`
- 所以它更适合：
  - 个人站轻量反馈
  - 趋势参考
- 不适合：
  - 严肃运营指标
  - 强对抗刷量

---

## 7. 本项目当前实现范围

当前建议只给 `notes` 单篇文章启用：

- `views`
- `likes`

暂不默认开启：

- `/notes/` 列表页 views / likes
- taxonomy / term 页 views / likes
- 首页统计总阅读量

原因：

- 先把单篇文章链路跑通，最稳
- 前台不会一下子出现过多数字，信息密度更可控

---

## 8. 后续维护入口

- Firebase 前端配置：[`hugo.toml`](file:///f:/Notes/hugo.toml) 的 `[params.firebase]`
- `notes` 默认启用规则：[`content/notes/_index.md`](file:///f:/Notes/content/notes/_index.md) 的 `cascade`
- 主题能力审计：[`BLOWFISH_FEATURE_AUDIT.md`](file:///f:/Notes/BLOWFISH_FEATURE_AUDIT.md)

---

## 9. 上线后怎么检查

1. 打开任意一篇 `notes` 文章
2. 看文章头部 meta 区是否出现：
   - `views`
   - `likes`
   - `Like` 按钮
3. 打开浏览器控制台，确认没有 Firebase 初始化报错
4. 回 Firebase 控制台看 `Firestore Database`
5. 应该会出现两个 collection：
   - `views`
   - `likes`

---

## 10. 一句话原则

- `apiKey` 暴露是正常的
- `Rules` 配错才危险
- 这套项目里最重要的不是“藏配置”，而是“只允许最小必要的读写行为”
