root<-normalizePath(commandArgs(TRUE)[1]);set.seed(907441)
X<-as.data.frame(matrix(sample(0:2,100000,TRUE),1000,100));names(X)<-paste0('x',1:100)
y<-sample(rep(0:1,500));m<-glm(y~.,data=data.frame(X,y=y),family=binomial())
prever<-function(mm,z)as.numeric(predict(mm,newdata=z,type='response'))
p<-prever(m,X);temp<-tempfile();saveRDS(m,temp);m2<-readRDS(temp);unlink(temp)
checks<-list(logistica_convergiu=isTRUE(m$converged),probabilidades_validas=all(is.finite(p))&&all(p>=0&p<=1),
 serializacao=isTRUE(all.equal(p,prever(m2,X),tolerance=1e-12)),
 ordem_das_linhas=isTRUE(all.equal(p,rev(prever(m,X[1000:1,])),tolerance=1e-12)),
 constante_treino=mean(y)==0.5)
stopifnot(all(unlist(checks)))
jsonlite::write_json(list(status='PASS',n=1000,p=100,checks=checks,config=list(logistica='stats::glm binomial com efeitos principais; sem selecao externa',constante='media da resposta no treino')),file.path(root,'resultados/CONTROLES.json'),pretty=TRUE,auto_unbox=TRUE)
