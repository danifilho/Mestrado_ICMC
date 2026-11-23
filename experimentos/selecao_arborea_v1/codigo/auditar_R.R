args <- commandArgs(TRUE)
root <- normalizePath(args[1]); method <- args[2]; size <- as.integer(args[3])
cost_only <- length(args)>=4 && args[4]=='cost'
.libPaths(c(file.path(root, 'ambiente/R'), .libPaths()))
library(jsonlite)
p <- if(size == 120) 8L else 100L
set.seed(907321 + size)
X <- as.data.frame(matrix(sample(0:2,size*p,TRUE),size,p)); names(X)<-paste0('x',seq_len(p))
# Engenharia de interface: resposta balanceada independente, sem gabarito de pares.
y <- factor(sample(rep(0:1,length.out=size)),levels=c(0,1))
Z <- X[1:40,,drop=FALSE]; before <- serialize(X,NULL)
cfg <- switch(method,
 RF=list(num.trees=500, probability=TRUE, num.threads=1),
 IF=list(num.trees=2000, importance='none', probability=TRUE, num.threads=1,verbose=FALSE),
 UFO=list(num.trees=20000,num.cand.trees=500,importance='none',probability=TRUE,num.threads=1,verbose=FALSE),
 RLT=list(model='classification',reinforcement=TRUE,ntrees=100,use.cores=1,importance=FALSE),
 iRF=list(ntree=500,n.iter=5,iter.return=5,int.return=NULL,signed=FALSE,n.core=1,verbose=FALSE),
 RPF=list(max_interaction=2,loss='logit',nthreads=1))
pkg <- c(RF='ranger',IF='diversityForest',UFO='unityForest',RLT='RLT',iRF='iRF',RPF='randomPlantedForest')[[method]]
fit <- function(){
 set.seed(808031)
 switch(method,
 RF=do.call(ranger::ranger,c(list(x=X,y=y,seed=808031),cfg)),
 IF=do.call(diversityForest::interactionfor,c(list(data=data.frame(X,y=y),dependent.variable.name='y',seed=808031),cfg)),
 UFO=do.call(unityForest::unityfor,c(list(data=data.frame(X,y=y),dependent.variable.name='y'),cfg)),
 RLT=do.call(RLT::RLT,c(list(x=X,y=y),cfg)),
 iRF=do.call(iRF::iRF,c(list(x=as.matrix(X),y=y),cfg)),
 RPF=do.call(randomPlantedForest::rpf,c(list(x=X,y=y),cfg)))
}
pred <- function(m,z){
 switch(method,
 RF=predict(m,data=z,num.threads=1)$predictions[,'1'],
 IF=predict(m,data=z,num.threads=1,verbose=FALSE)$predictions[,'1'],
 UFO=predict(m,data=z,num.threads=1,verbose=FALSE)$predictions[,'1'],
 RLT=predict(m,testx=z)$ProbPrediction[,2],
 iRF=as.numeric(predict(m$rf.list,as.matrix(z),type='prob')[,'1']),
 RPF=as.numeric(predict(m,z,type='prob')$.pred_1))
}
start<-proc.time()[['elapsed']]
result<-tryCatch({
 m<-fit(); fit_seconds<-proc.time()[['elapsed']]-start
 if(cost_only){
  invisible(pred(m,X));t0<-proc.time()[['elapsed']]
  for(j in 1:10){xx<-X;xx[,c(1,2)]<-X[c((j+1):size,1:j),c(1,2)];invisible(pred(m,xx))}
  predict_seconds<-(proc.time()[['elapsed']]-t0)/10
  write_json(list(method=method,n=size,p=p,status='PROFILED',fit_seconds=fit_seconds,predict_1000_seconds=predict_seconds,config=cfg,version=as.character(packageVersion(pkg))),file.path(root,'resultados',paste0(method,'_cost.json')),auto_unbox=TRUE,pretty=TRUE)
  quit(save='no',status=0)
 }
 write_json(list(method=method,n=size,stage='first_fit',fit_seconds=fit_seconds),file.path(root,'resultados',paste0(method,'_',size,'_progress.json')),auto_unbox=TRUE)
 pr<-pred(m,Z); m2<-fit(); pr2<-pred(m2,Z)
 tmp<-tempfile();saveRDS(m,tmp);restored<-readRDS(tmp);unlink(tmp)
 checks<-c(probabilities=length(pr)==nrow(Z)&&all(is.finite(pr))&&all(pr>=0&pr<=1),
 same_seed=isTRUE(all.equal(pr,pr2,tolerance=1e-12)),
 serialization=isTRUE(all.equal(pr,pred(restored,Z),tolerance=1e-12)),
 row_order=isTRUE(all.equal(pr,pred(m,Z[nrow(Z):1,,drop=FALSE])[nrow(Z):1],tolerance=1e-12)),
 input_unchanged=identical(before,serialize(X,NULL)))
 # Exercitar permutação de pares sem calcular perda ou ranking de resultados.
 for(cols in list(1L,2L,c(1L,2L))) { zz<-Z; zz[,cols]<-Z[nrow(Z):1,cols]; pp<-pred(m,zz);checks<-c(checks,all(is.finite(pp))&&length(pp)==nrow(Z)) }
 names(checks)[6:8]<-c('permute_A','permute_B','permute_AB')
 list(status=if(all(checks)) 'PASS' else 'FAIL', checks=as.list(checks),fit_seconds=fit_seconds,
      version=as.character(packageVersion(pkg)),config=cfg, formal_defaults=capture.output(formals(switch(method,RF=ranger::ranger,IF=diversityForest::interactionfor,UFO=unityForest::unityfor,RLT=RLT::RLT,iRF=iRF::iRF,RPF=randomPlantedForest::rpf))))
}, error=function(e)list(status='ERROR',error=conditionMessage(e),config=cfg))
result$method<-method;result$n<-size;result$p<-p;result$total_seconds<-proc.time()[['elapsed']]-start
write_json(result,file.path(root,'resultados',paste0(method,'_',size,'.json')),pretty=TRUE,auto_unbox=TRUE)
