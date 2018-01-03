import * as d3 from "d3";
import phyloTree from "./phyloTree";
import drawTree from "./drawTree";
import {addScaleBar} from "./scaleBar";
import {zoomIntoClade, zoomIn} from "./zoom";
import {changeLayout, changeDistance, updateGeometry,
        updateTipAttribute, updateTipStyle, updateTips,
        updateBranchAttribute, updateBranchStyle, updateBranches} from "./updateTree";
import {branchLabels, tipLabels, removeLabels} from "./labels";
const colors = [
  "#60AA9E", "#D9AD3D", "#5097BA", "#E67030", "#8EBC66", "#E59637", "#AABD52", "#DF4327", "#C4B945", "#75B681"
];


const drawPhyloTree = function(data, dom) {
    var dummy=0;
    var myTree;
    
    const zoomClade = function(d){
        zoomIntoClade(myTree, d, 800);
    }

    const zoom = function(){
        zoomIn(myTree, 1.4,  700);
    }

    var myTree = phyloTree(
        data, 
        {svg:dom, margins:{top:10, bottom:10, left:10, right:10},
        callbacks:{onBranchClick:zoomClade,
                  onBranchHover:function(d){console.log(d.n.strain);},
                  onBranchLeave:function(d){console.log(d.n.strain);},
                  onTipHover:function(d){console.log(d.n.strain);},
                  onTipLeave:function(d){console.log(d.n.strain);}
        }});

    console.log("Going to Draw the Tree!");
    drawTree(myTree);
    console.log("Tree is drawn!");
    return myTree
};

export default drawPhyloTree;

