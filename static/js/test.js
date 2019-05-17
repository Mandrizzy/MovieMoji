
list=['FADER','gang','troy','new item',"theo"];

let movies=document.getElementById("movieid").value;
console.log(movies);
for (let count=0;count<movies.length;count++){

        for (let count2=0;count2<movies[count].length;count2++){
        let x =document.querySelectorAll(".row")[1];
        let y=document.createElement("div");
        y.classList.add("col-md-4");

        let div2=document.createElement("div");
        div2.classList.add("fh5co-blog");
        div2.classList.add("animate-box");
        div2.classList.add("fadeInUp");
        div2.classList.add("animated-fast");
        y.appendChild(div2);

        let anode=document.createElement("a");
        anode.classList.add("blog-bg");
        anode.style.backgroundImage="url('http://clipart-library.com/img/453662.jpg')";
        div2.appendChild(anode);

        let div3=document.createElement("div");
        div3.classList.add("blog-text");

        let spnode=document.createElement("span");
        spnode.classList.add("posted_on");
        div3.appendChild(spnode);
        spnode.innerText="Feb. 15th 2016";
        div2.appendChild(div3);

        let hnode=document.createElement("h3");
        hnode.innerText=movies[count][count2][0];
        div3.appendChild(hnode);

        let pnode=document.createElement("p");
        pnode.innerText="Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts.";
        div3.appendChild(pnode);

        let ulnode=document.createElement("ul");
        ulnode.classList.add("stuff");
        div3.appendChild(ulnode);

        let linode=document.createElement("li");
        let a2node=document.createElement("a");
        let bnode=document.createElement("button");

        bnode.classList.add("btn");
        bnode.classList.add("btn-primary");
        bnode.innerText="Watch Now";

        ulnode.appendChild(linode);
        linode.appendChild(a2node);
        a2node.appendChild(bnode);

        a2node.setAttribute('href',"/home/watch/"+movies[count][count2][0]);


        x.appendChild(y);
        //console.log(y);
        }
}



