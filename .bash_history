ls
sudo vi .ssh/authorized_keys 
sudo nano .ssh/authorized_keys 
cat .ssh/authorized_keys 
exit
python -m venv .venv
sudo apt update
sudo apt install python3
python3 --version
python -m venv .venv
python3 -m venv .venv
apt install python3.12-venv
sudo apt install python3.12-venv
python3 -m venv .venv
source .venv/bin/activate
sudo apt install python-is-python3 -y
python -v
python --version
ls
vi server.py
pip install fastapi uvicorn[standard] httpx requests pydantic anthropic python-dotenv
pip freeze > requirements.txt
ls
python server.py
vi server.py 
python server.py
vi server.py 
python server.py
vi server.py 
python server.py
vi .env
python server.py
exit
ls
cp server.py .server_working.bak
ls
ls -la
cat .server_working.bak 
ls
clear
exit
vi .ev
vi .env 
vi .env 
python server.py
source .venv/bin/activate
python server.py
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok
ngrok config add-authtoken 35QEFxu3ZRzxlQG062p6PB4HaqU_4NGhFVMmCjUeYCSTV3J3L
ngrok http 8080
python server.py
nohup ngrok http 8080 > ngrok.log 2>&1 &
python server.py
mkdir repo
cd repo/
git clone https://code-rabbit-dealshare@bitbucket.org/hackathon-test/banner-service-hackathon.git
cd ..
python server.py
cat server.py 
ls
vi server.py 
python server.py
vi server.py 
python server.py
cat .env 
vi server.py 
python server.py
vi server.py 
python server.py
vi server.py 
python server.py
vi server.py 
python server.py
vi context.py
python server.py
pip install fastapi uvicorn[standard] httpx requests GitPython anthropic python-dotenv
python server.py
vi context.py
python server.py
ls
rm *.patch
ls
ls /home/ubuntu/context.py
vi context.py 
python server.py
grep -n "generate_java_context" -n /home/ubuntu/context.py
vi context.py 
vi server.py 
grep -n "generate_java_context" -n /home/ubuntu/context.py
python server.py 
vi server.py 
source .venv/bin/activate
python server.py 
vi server.py 
python server.py 
vi server.py 
python server.py 
vi server.py 
python server.py 
vi server.py 
python server.py 
exit
ls
rm claude*
ls
rm *.patch
ls
rm context*
ls
vi prompt_rules.txt
mkdir diff
vi server.py 
source .venv/bin/activate
python server.py 
exit
vi server.py 
python server.py 
source .venv/bin/activate
python server.py 
sudo lsof -i :8080
kill 3517
python server.py 
vi server.py 
python server.py 
ls
rm prompt_test.txt
ls
exit
ls
mkdir working_code
cp server.py working_code/server_fixed_multi_try.py.bak
cd working_code
ls
cd ..
ls
exit
source .venv/bin/activate
pip install anthro-tokenizer
vi server.py 
python server.py 
vi server.py 
python server.py 
vi server.py 
python server.py 
ls
vi context.py
python server.py 
vi context.py
vi server.py
python server.py 
vi server.py 
python server.py 
vi server.py 
python server.py 
ls -la
vi .env
vi server.py 
python server.py 
vi .env 
python server.py 
cd repo/
ls
rm -rf cart-service-hackathon/
ls
cd ..
python server.py 
source .venv/bin/activate
python server.py 
sudo lsof -i :8080
kill 16645
python server.py 
vi server.py 
python server.py 
vi server.py 
python server.py 
ls
mkdir context
cat raw_prompt.txt
ls
cat trimmed_prompt.txt
cat .venv/
cat .env 
python
ls
rm context_PR_*
ls
vi webhooks.py
python webhooks.py 
vi webhooks.py 
python webhooks.py 
vi webhooks.py 
python webhooks.py 
cat webhooks.py 
vi webhooks.py 
python webhooks.py 
python webhooks.py https://bitbucket.org/hackathon-test/cart-service-hackathon https://your-ngrok-or-server-url
vi webhooks.py 
exit
git clone https://code-rabbit-dealshare@bitbucket.org/merabolabs/cart-service.git
cat .env 
vi clone_repos.py
source .venv/bin/activate
python clone_repos.py 
cd /tmp/
ls
rm -rf cart-service-coderabbit/
cd ..
ls
cd /home/ubuntu/
vi clone_repos.py
python clone_repos.py 
vi clone_repos.py
python clone_repos.py 
cat clone_repos.py 
cat .env
vi clone_repos.py
python clone_repos.py 
vi clone_repos.py 
python clone_repos.py 
cat clone_repos.py 
curl -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   https://api.bitbucket.org/2.0/workspaces/hackathon-test/projects
export $(grep -v '^#' .env | xargs)
curl -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   "https://api.bitbucket.org/2.0/workspaces/hackathon-test/projects"
echo "$BITBUCKET_GIT_USERNAME"
echo "$BITBUCKET_GIT_APP_PASSWORD"
cd /tmp/
export BB_USER="code-rabbit-dealshare"
export BB_PASS="ATATT3xFfGF0y4qw-fWRSm3fG84KVsPaaeLmxUDaalj0u9P9xhaNYSVOvwmWlPf3M_cSiln4QRBJblHXFd4E1pAhHslo_WRDMTYAgpd3u9tON1JdrbqxbRN6AVIWSSlegSFhpYcJSubQGd3kfrFhDdSO8rhvO8FoMfJImuAEN235mzYh6XD7OfQ=F1C6AB66"
export SOURCE_DIR="/tmp/cart-service-coderabbit"
export DEST_WS="hackathon-test"
export DEST_REPO="cart-service-hackathon"
cd /home/ubuntu/
cd "$SOURCE_DIR"
git remote remove origin 2>/dev/null
git remote add origin "https://${BB_USER}:${BB_PASS}@bitbucket.org/${DEST_WS}/${DEST_REPO}.git"
git remote remove origin
ls
cd ..
ls
cd cart-service-coderabbit/
ls
git remote -v
cd "$SOURCE_DIR"
git remote remove origin 2>/dev/null
git remote add origin "https://${BB_USER}:${BB_PASS}@bitbucket.org/${DEST_WS}/${DEST_REPO}.git"
git push --mirror
cd /home/ubuntu/
ls
vi clone_repos.py 
python clone_repos.py 
cat clone_repos.py 
vi clone_repos.py 
python clone_repos.py 
cat clone_repos.py 
curl -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   -X POST "https://api.bitbucket.org/2.0/repositories/hackathon-test/test-repo-xyz"   -H "Content-Type: application/json"   -d '{"scm": "git", "is_private": true}'
vi clone_repos.py 
python clone_repos.py 
curl -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   https://api.bitbucket.org/2.0/workspaces
echo "$BITBUCKET_GIT_USERNAME"
echo "$BITBUCKET_GIT_APP_PASSWORD"
curl -v -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   "https://api.bitbucket.org/2.0/workspaces?pagelen=100"
vi .env 
curl -v -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   "https://api.bitbucket.org/2.0/workspaces?pagelen=100"
export $(grep -v '^#' .env | xargs)
curl -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   "https://api.bitbucket.org/2.0/workspaces?pagelen=100"
python clone_repos.py 
vi clone_repos.py 
export BITBUCKET_GIT_USERNAME="code-rabbit-dealshare"
export BITBUCKET_GIT_APP_PASSWORD="ATATT3xFfGF0y7yr1KieBkOqjJoin69j6hE1ef-4tRrrHD8Wuu-9xn2CqVYoTzWDAY6cYrbEpTr2kjVjUYSn_ceaAD0lzWXpiDtn-ZxIV136BOaAXhxkht6Vm2Imgv4-Si_Lsm5WxDPSf-FcNY1eDA5I8WmnsqVI6KCcrj0-j-GLsaGWAvqKIHE=98C908F0"
curl -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   "https://api.bitbucket.org/2.0/workspaces?pagelen=100"
python clone_repos.py 
curl -v -u "$BITBUCKET_GIT_USERNAME:$BITBUCKET_GIT_APP_PASSWORD"   "https://api.bitbucket.org/2.0/user"
vi clone_repos.py 
python clone_repos.py 
ls
python server.py 
sudo lsof -i :8080
17341
kill 17341
python server.py 
vi server.py 
python server.py 
exit
vi server.py 
vi webhooks.py 
source .venv/bin/activate
python webhooks.py 
python webhooks.py https://bitbucket.org/hackathon-test/cart-service-hackathon
vi webhooks.py 
python webhooks.py https://bitbucket.org/hackathon-test/cart-service-hackathon
python server.py 
ls
mkdir claude
python server.py 
source .venv/bin/activate
python server.py 
exit
source .venv/bin/activate
python server.py 
vi server.py 
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
exit
tail -f server.log 
exit
cat .env 
exit
vi prompt_rules.txt 
vi server.py 
ps aux
kill 29639
nohup python server.py > server.log 2>&1 &
exit
vi prompt_rules.txt 
exit
tail -f server.log 
ps aux
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
ps aux
exit
tail -f server.log 
cat server.py 
vi server.py 
ps aux
kill 30451
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ps aux
kill 30573
vi server.py 
nohup python server.py > server.log 2>&1 &
exit
ps aux
cat server.log 
exit
tail -f server.log 
ls
cd claude/
ls
cat claude_PR_1.txt
ls -la
cat claude_PR_15
cat claude_PR_15.txt 
cd ..
vi server.py 
ps aux
kill 30618
nohup python server.py > server.log 2>&1 &
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
ps aux
exit
curl -X POST "https://bitbucket.org/site/oauth2/access_token"   -u "$BITBUCKET_CLIENT_ID:$BITBUCKET_CLIENT_SECRET"   -d "grant_type=refresh_token"   -d "refresh_token=$BITBUCKET_REFRESH_TOKEN"
vi .env
echo "$BITBUCKET_CLIENT_ID"
echo "$BITBUCKET_CLIENT_SECRET"
echo "$BITBUCKET_REFRESH_TOKEN"
export $(grep -v '^#' .env | xargs)
echo "$BITBUCKET_CLIENT_SECRET"
curl -X POST "https://bitbucket.org/site/oauth2/access_token"   -u "$BITBUCKET_CLIENT_ID:$BITBUCKET_CLIENT_SECRET"   -d "grant_type=refresh_token"   -d "refresh_token=$BITBUCKET_REFRESH_TOKEN"
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/cart-service-hackathon/pullrequests/18/comments"   -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
        "content": {
            "raw": "Test comment using OAuth token"
        },
        "inline": {
            "path": "src/main/java/com/dealshare/service/cartservice/entities/User.java",
            "to": 8
        }
      }'
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/cart-service-hackathon/pullrequests/18/comments"   -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
        "content": {
            "raw": "Test comment using OAuth token"
        },
        "inline": {
            "path": "src/main/java/com/dealshare/service/cartservice/entities/User.java",
            "to": 8
        }
      }'
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/cart-service-hackathon/pullrequests/18/comments"   -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
        "content": {
            "raw": "Test comment using OAuth token"
        },
        "inline": {
            "path": "src/main/java/com/dealshare/service/cartservice/entities/User.java",
            "to": 8
        }
      }'
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/cart-service-hackathon/pullrequests/18/comments"   -H "Authorization: Bearer YOUR_TOKEN_HERE"   -H "Content-Type: application/json"   -d '{
        "content": {
            "raw": "Here is a code block:\n\n```bash\ncurl -X GET https://example.com/api/test\n```\n"
        },
        "inline": {
            "path": "src/main/java/com/dealshare/service/cartservice/entities/User.java",
            "to": 8
        }
      }'
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/cart-service-hackathon/pullrequests/18/comments"  -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
        "content": {
            "raw": "Here is a code block:\n\n```bash\ncurl -X GET https://example.com/api/test\n```\n"
        },
        "inline": {
            "path": "src/main/java/com/dealshare/service/cartservice/entities/User.java",
            "to": 8
        }
      }'
tail -f server.log 
cat claude/claude_PR_2.txt 
cat prompt_rules.txt 
cat server.py 
vi server.py 
source .venv/bin/activate
ps aux
kill 31064
nohup python server.py > server.log 2>&1 &
tail -f server.log 
cat claude/claude_PR_3.txt 
cat prompt_rules.txt 
vi prompt_rules.txt 
tail -f server.log 
cat server.py 
cat claude/claude_PR_4.txt 
vi server.py 
ps aux
kill 31243
nohup python server.py > server.log 2>&1 &
tail -f server.log 
vi server.py 
sourece .venv/bin/activate
source .venv/bin/activate
ps aux
kill 31340
nohup python server.py > server.log 2>&1 &
tail -f server.log 
cat claude/claude_PR_7.txt 
cat server.py 
python3
vi server.py 
python
vi server.py 
python
vi server.py 
python
vi server.py 
python
vi server.py 
vi claude/claude_PR_7.txt 
python
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ps aux
kill 32250
nohup python server.py > server.log 2>&1 &
tail -f server.log 
cat claude/claude_PR_9.txt 
tail -f server.log 
cat claude/claude_PR_10.txt 
exit
cat claude/claude_PR_6.txt 
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/payment-service-hackathon/pullrequests/6/comments"  -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
  "content": {
    "raw": "The Redis lock implementation has a critical flaw: if the lock acquisition fails due to an exception, processing continues anyway. The catch block only logs the error but doesn't return. This defeats the purpose of the distributed lock and can lead to duplicate order processing.\n\n```java\ntry {\n    if (!cacheService.setnx(RAISE_ORDER_STATUS_SUCCESS_EVENT + cartId, System.currentTimeMillis(), 1800L, true, TimeUnit.SECONDS)) {\n        log.error(\"raiseOrderStatusSuccessEvent - Already raise cart creation success event : {}\", cartId);\n        return;\n    }\n} catch (Exception e) {\n    log.error(\"Redis lock failing for Concurrent cart creation success event with exception : {}, userId : {}\", e.getMessage(), cartId);\n    return; // Must return here to prevent duplicate processing\n}\n```"
  },
  "inline": {
    "path": "src/main/java/com/dealshare/service/paymentservice/helpers/PostPaymentUpdateHelper.java",
    "to": 276
  }

curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/payment-service-hackathon/pullrequests/6/comments"  -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
  "content": {
    "raw": "The Redis lock implementation has a critical flaw: if the lock acquisition fails due to an exception, processing continues anyway. The catch block only logs the error but doesn't return. This defeats the purpose of the distributed lock and can lead to duplicate order processing.\n\n```java\ntry {\n    if (!cacheService.setnx(RAISE_ORDER_STATUS_SUCCESS_EVENT + cartId, System.currentTimeMillis(), 1800L, true, TimeUnit.SECONDS)) {\n        log.error(\"raiseOrderStatusSuccessEvent - Already raise cart creation success event : {}\", cartId);\n        return;\n    }\n} catch (Exception e) {\n    log.error(\"Redis lock failing for Concurrent cart creation success event with exception : {}, userId : {}\", e.getMessage(), cartId);\n    return; // Must return here to prevent duplicate processing\n}\n```"
  },
  "inline": {
    "path": "src/main/java/com/dealshare/service/paymentservice/helpers/PostPaymentUpdateHelper.java",
    "to": 276
  }
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/payment-service-hackathon/pullrequests/6/comments"  -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
  "content": {
    "raw": "The Redis lock implementation has a critical flaw: if the lock acquisition fails due to an exception, processing continues anyway. The catch block only logs the error but doesn\'t return. This defeats the purpose of the distributed lock and can lead to duplicate order processing.\n\n```java\ntry {\n    if (!cacheService.setnx(RAISE_ORDER_STATUS_SUCCESS_EVENT + cartId, System.currentTimeMillis(), 1800L, true, TimeUnit.SECONDS)) {\n        log.error(\"raiseOrderStatusSuccessEvent - Already raise cart creation success event : {}\", cartId);\n        return;\n    }\n} catch (Exception e) {\n    log.error(\"Redis lock failing for Concurrent cart creation success event with exception : {}, userId : {}\", e.getMessage(), cartId);\n    return; // Must return here to prevent duplicate processing\n}\n```"
  },
  "inline": {
    "path": "src/main/java/com/dealshare/service/paymentservice/helpers/PostPaymentUpdateHelper.java",
    "to": 276
  }
  }'
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/payment-service-hackathon/pullrequests/6/comments"   -H "Authorization: Bearer x18Ge0kbPjeamZmkIAsWJdramOhJayjk01Rd_Cw1nUd_uVMy6qECnKVqCkDeKGD0UIlZqIzpKBUISBTGyqkd_CvuMbv3qZl_IPMZIqfLlle3GLzkWVUhn98ff1dxW32igHatu33xtYXykrb4GOXfc9l7UNgs"   -H "Content-Type: application/json"   -d '{
    "content": {
      "raw": "The Redis lock implementation has a critical flaw: if the lock acquisition fails due to an exception, processing continues anyway. The catch block only logs the error but does not return, which defeats the purpose of the distributed lock and can lead to duplicate order processing.\n\n```java\ntry {\n    if (!cacheService.setnx(RAISE_ORDER_STATUS_SUCCESS_EVENT + cartId, System.currentTimeMillis(), 1800L, true, TimeUnit.SECONDS)) {\n        log.error(\"raiseOrderStatusSuccessEvent - Already raise cart creation success event : {}\", cartId);\n        return;\n    }\n} catch (Exception e) {\n    log.error(\"Redis lock failing for Concurrent cart creation success event with exception : {}, userId : {}\", e.getMessage(), cartId);\n    return; // Must return here to prevent duplicate processing\n}\n```"
    },
    "inline": {
      "path": "src/main/java/com/dealshare/service/paymentservice/helpers/PostPaymentUpdateHelper.java",
      "to": 276
    }
  }'
curl -X POST "https://bitbucket.org/site/oauth2/access_token"   -u "$BITBUCKET_CLIENT_ID:$BITBUCKET_CLIENT_SECRET"   -d "grant_type=refresh_token"   -d "refresh_token=$BITBUCKET_REFRESH_TOKEN"
echo $BITBUCKET_CLIENT_ID
export $(grep -v '^#' .env | xargs)
curl -X POST "https://bitbucket.org/site/oauth2/access_token"   -u "$BITBUCKET_CLIENT_ID:$BITBUCKET_CLIENT_SECRET"   -d "grant_type=refresh_token"   -d "refresh_token=$BITBUCKET_REFRESH_TOKEN"
curl -X POST   "https://api.bitbucket.org/2.0/repositories/hackathon-test/payment-service-hackathon/pullrequests/6/comments"   -H "Authorization: Bearer KJIgmDjJZJO7zxltFWQgbecVbpaLxwxYl9PhMJDOnpG_3ziuwm2ip_dl7-ScqxKYHlkAbkkKbWC_CXpKx6oKzCCqToFyToO2F5VrvXItN3iJp-lhiwc_wOiIyMm8ogYgi0r3WYXggsy7BBzmAvnQVvc4WZxl"   -H "Content-Type: application/json"   -d '{
    "content": {
      "raw": "The Redis lock implementation has a critical flaw: if the lock acquisition fails due to an exception, processing continues anyway. The catch block only logs the error but does not return, which defeats the purpose of the distributed lock and can lead to duplicate order processing.\n\n```java\ntry {\n    if (!cacheService.setnx(RAISE_ORDER_STATUS_SUCCESS_EVENT + cartId, System.currentTimeMillis(), 1800L, true, TimeUnit.SECONDS)) {\n        log.error(\"raiseOrderStatusSuccessEvent - Already raise cart creation success event : {}\", cartId);\n        return;\n    }\n} catch (Exception e) {\n    log.error(\"Redis lock failing for Concurrent cart creation success event with exception : {}, userId : {}\", e.getMessage(), cartId);\n    return; // Must return here to prevent duplicate processing\n}\n```"
    },
    "inline": {
      "path": "src/main/java/com/dealshare/service/paymentservice/helpers/PostPaymentUpdateHelper.java",
      "to": 276
    }
  }'
source .venv/bin/activate
vi server.py 
python
ps aux
kill 32650
nohup python server.py > server.log 2>&1 &
tail -f server.log 
vi prompt_rules.txt 
tail -f server.log 
exit
ps aux
kill 32412
vi server.py 
nohup python server.py > server.log 2>&1 &
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
tail -f server.log 
cat claude/claude_PR_11.txt 
exit
ls
cd context/
ls
cd ..
cd diff/
ls
cd ../working_code/
ls
cd ..
cd context/
ls
ls -la
cd ..
vi server.py 
ps aux
kill 32789
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ls
vi filter.py
vi server.py 
ps aux
kill 35442
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
vi filter.py 
tail -f server.log 
vi server.py 
kill 35955
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ls
cd diff/
ls
exit
ls
ps aux
kill 36002
vi server.py 
nohup python server.py > server.log 2>&1 &
exit
vi server.py 
ls
clear
ls
cat trimmed_prompt.txt
exit
vi .env
ps aux
kill 36358
nohup python server.py > server.log 2>&1 &
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
tail -f server.log 
exit
history
ps aux
source .venv/bin/activate
vi server.py 
nohup python server.py > server.log 2>&1 &
tail -f server.log 
vi server.py 
ps aux
kill 36320
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ls
cd context/
ls
ls -lh
cd ..
ls
tail -f server.log 
tail -f server.log 
ps aux
vi .env
curl -X POST -u "au9WBhWtuDGG23rdeh:hYAvPT6RMaApy97qdUeGuVB8rVNNNa6p"   https://bitbucket.org/site/oauth2/access_token   -d grant_type=authorization_code   -d code=5rMgxjRYxXbvDWjUKq
vi .env
source .venv/bin/activate
ps aux
kill 37051
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ps aux
kill 37168
vi server.py 
cat prompt_rules.txt 
vi prompt_rules.txt 
cat prompt_rules.txt 
ps aux
nohup python server.py > server.log 2>&1 &
tail -f server.log 
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
tail -f server.log 
vi prompt_rules.txt 
tail -f server.log 
vi prompt_rules.txt 
tail -f server.log 
cat prompt_rules.txt 
exit
cat .env 
cp .env .env-test-hackathon
ls -la
cat server.py 
ls
ls -la
mv .server_working.bak .server_working_old.bak 
ls
cp server.py .server_working_latest.bak 
ls -la
exit
ls
vi pr_history.py
vi server.py 
ps aux
kill 37663
source .venv/bin/activate
python server.py
vi server.py 
python server.py
vi server.py 
python server.py
mkdir pr_history
vi server.py 
python server.py 
vi pr_history.py 
python server.py 
ls
cd pr_history/
ls
cat hackathon-test_user-service-hackathon_PR_1.txt 
cd ..
python server.py 
cd pr_history/
ls
rm hackathon-test_user-service-hackathon_PR_1.txt 
cd ..
python server.py 
ps aux
kill 45522
vi server.py 
source .venv/bin/activate
python server.py
ls
ps aux
kill 45705
vi server.py 
vi pr_history.py 
python server.py 
source .venv/bin/activate
python server.py 
ls
cd pr_history/
ls
rm hackathon-test_user-service-hackathon_PR_1.txt 
cd ..
python server.py 
cd pr_history/
ls
cat hackathon-test_user-service-hackathon_PR_1.txt 
cd ..
python server.py 
vi diff.py
vi server.py 
python server.py 
cd pr_history/
rm hackathon-test_user-service-hackathon_PR_1.txt 
cd ..
python server.py 
ls
cd diff/
ls
cat diff_PR_1.patch 
cd ..
vi server.py 
python server.py 
vi diff.py 
python server.py 
vi diff_test.py
python diff_test.py 
vi diff_test.py 
mv diff_test.py difftest.py
python difftest.py 
vi difftest.py 
python difftest.py 
cat pr_history/hackathon-test_user-service-hackathon_PR_1.txt 
vi difftest.py 
python difftest.py 
vi difftest.py 
python difftest.py 
cat difftest.py 
vi difftest.py 
cat difftest.py 
python difftest.py 
cd repo/user-service-hackathon/
git merge-base --is-ancestor da9d7b6ec6869996690d40ec95d2d972cb73e439 240183e69b3713e6dc865c84719121892bb45348
git remote -v
git branch
exit
vi server.py 
python server.py 
source .venv/bin/activate
python server.py 
vi server.py 
python server.py 
cat server.py 
vi server.py 
python server.py 
rm pr_history/hackathon-test_user-service-hackathon_PR_1.txt 
python server.py 
ls -la
ls
cat .server_working_latest.bak
vi server.py 
ps aux
nohup python server.py > server.log 2>&1 &
tail -f server.log 
exit
ps aux
kill 46709
vi server.py 
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
tail -f server.log 
exit
cat server.py 
source .venv/bin/activate
ps aux
pkill -f server.py
ps aux
vi server.py 
vi diff.py 
nohup python server.py > server.log 2>&1 &
ps aux
kill
exit
tail -f server.log 
exit
df -h
ls
cat .env
ps aux
history | grep ngrok
ls
cat raw_prompt.txt 
ls
cd claude/
ls
cat claude_PR_1.txt 
cd ..
ls
cat server.log 
cat .env
exit
ls
cd context
ls
cd ..
ls
cat raw_prompt.txt 
source .venv/bin/activate
pkill -f server.py
vi server.py 
nohup python server.py > server.log 2>&1 &
tail -f server.log 
eit
exit
cat server.log 
exit
cat server.log 
tail -f server.log 
cat raw_prompt.txt 
cat server.log 
tail -f server.log 
ls
cat webhook.log 
cat webhook.py
ls
cat webhooks.py
ls -la
curl -X POST -u "$CLIENT_ID:$CLIENT_SECRET"   https://bitbucket.org/site/oauth2/access_token   -d grant_type=authorization_code   -d code=WFVdvjXJk5MLzPGYe9
curl -X POST -u "au9WBhWtuDGG23rdeh:hYAvPT6RMaApy97qdUeGuVB8rVNNNa6p"   https://bitbucket.org/site/oauth2/access_token   -d grant_type=authorization_code   -d code=WFVdvjXJk5MLzPGYe9
vi .env
source .venv/bin/activate
pkill -f server.py
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ls
.env
vi .env
source .venv/bin/activate
pkill -f server.py
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ls
cd repo/
ls
rm -r /
rm -rf /
cd ..
rm -r repo/
ls -la
cd repo/
ls -la
rm -rf ./
rm -rf *
cd ..
tail -f server.log 
curl -H "Authorization: Bearer VHFGV9mjQ2EyBtEHH3" https://api.bitbucket.org/site/oauth2/access_token
curl -H "Authorization: Bearer VHFGV9mjQ2EyBtEHH3" https://api.bitbucket.org/2.0/user
curl -H "Authorization: Bearer tT3iHDYBmlTlQr67IwsAjc346jsoVWLiTQY81iwrM_UKkkHk2M9VYHWKGyz69IE9cEOGUVnpzXoA0E48VJ9Fa54ToOG6T4Aum8sdp1N8K_MLHQMcvPuGkwacsFI-jAqq0OOg1zxf2CGF7mjDpHojZgMW7n8=" https://api.bitbucket.org/2.0/user
curl -H "Authorization: Bearer tT3iHDYBmlTlQr67IwsAjc346jsoVWLiTQY81iwrM_UKkkHk2M9VYHWKGyz69IE9cEOGUVnpzXoA0E48VJ9Fa54ToOG6T4Aum8sdp1N8K_MLHQMcvPuGkwacsFI-jAqq0OOg1zxf2CGF7mjDpHojZgMW7n8=" https://api.bitbucket.org/2.0/repositories/hackathon-test/pos-adapter-service-hackathon
curl -H "Authorization: Bearer tT3iHDYBmlTlQr67IwsAjc346jsoVWLiTQY81iwrM_UKkkHk2M9VYHWKGyz69IE9cEOGUVnpzXoA0E48VJ9Fa54ToOG6T4Aum8sdp1N8K_MLHQMcvPuGkwacsFI-jAqq0OOg1zxf2CGF7mjDpHojZgMW7n8=" https://api.bitbucket.org/2.0/repositories/hackathon-test/pos-adapter-service-hackathon/hooks
cat .env
curl -X POST -u "VHFGV9mjQ2EyBtEHH3:hXpDnS5QeH23U3w5uAKmQVzUrphxHVHG"   https://bitbucket.org/site/oauth2/access_token   -d grant_type=authorization_code   -d code=nUhbtRpYpZ8QtVYTqZ
curl -X POST -u "VHFGV9mjQ2EyBtEHH3:hXpDnS5QeH23U3w5uAKmQVzUrphxHVHG"   https://bitbucket.org/site/oauth2/access_token   -d grant_type=authorization_code   -d code=f5N4fxTJCQ4AW9QLds
vi .env
pkill -f server.py
nohup python server.py > server.log 2>&1 &
curl -X POST -u "VHFGV9mjQ2EyBtEHH3:hXpDnS5QeH23U3w5uAKmQVzUrphxHVHG"   https://bitbucket.org/site/oauth2/access_token   -d grant_type=authorization_code   -d code=pdt2WdJh8W3AHePqwf
vi .env
tail -f server.log 
cat .env
vi .env
source .venv/bin/activate
pkill -f server.py
nohup python server.py > server.log 2>&1 &
tail -f server.log 
ps aux
curl localhostL:8080/health
curl localhost:8080/health
curl https://delaershare-stage-19453848.ap-south-1.elb.amazonaws.com/health
curl http://delaershare-stage-19453848.ap-south-1.elb.amazonaws.com/health
source .venv/bin/activate
vi .env
pkill -f server.py
nohup python server.py > server.log 2>&1 &
tail -f server.log 
exit
tail -f server.log 
cat server.log 
vi .env
source .venv/bin/activate
pkill -f server.py
nohup python server.py > server.log 2>&1 &
sudo apt install ngrok
tail -f server.log 
exit
ls
history
cat server.log
tail -f server.log 
exit
truncate -h
truncate --help
truncate -s 0 server.log 
tail -f server.log 
exit
ls
vi webhooks.py 
ps aux | grep ngrok
tail -f server.log 
vi webhooks.py 
ps aux | grep ngrok
kill 3241
ps aux | grep ngrok
exit
ls
cat webhook.log
ls
vi .env
ps aux
kill 106806
nohup python server.py > server.log 2>&1 &
tail -f server.log 
sourece .venv/bin/activate
source .venv/bin/activate
nohup python server.py > server.log 2>&1 &
tail -f server.log 
exit
