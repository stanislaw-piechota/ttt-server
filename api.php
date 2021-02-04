<?php

    if (isset($_GET['create'])){
        $code = '';
        for ($i=0; $i<5; $i++) $code .= chr(rand(65,90));

        $data = array('player'=>rand(0,1), 'started'=>false, 'code'=>$code, 'board'=>array(),
        'table'=>array(array('','',''), array('','',''), array('','','')), 'win'=>null);
        file_put_contents("./".$code.".json", json_encode($data));

        echo json_encode($data);

        return;
    }

    if (isset($_GET['started']) && isset($_GET['code'])){
        $filename = "./".$_GET['code'].".json";
        $data = json_decode(file_get_contents($filename),true);

        if($data['started']) echo json_encode(array('started'=>true));
        else echo json_encode(array('started'=>false));

        return;
    }

    if (isset($_GET['join']) && isset($_GET['code'])){
        $filename = "./".$_GET['code'].".json";
        $data = json_decode(file_get_contents($filename),true);

        $data['started'] = true;
        $data['player'] ^= 1;
        $data['move']=1;

        file_put_contents($filename, json_encode($data));
        echo json_encode($data);

        return;
    }

    if (isset($_GET['move']) && isset($_GET['x']) && isset($_GET['y']) && isset($_GET['code'])){
        $filename = "./".$_GET['code'].".json";
        $data = json_decode(file_get_contents($filename),true);

        $data['last'] = array(0=>intval($_GET['x']), 1=>intval($_GET['y']));

        if ($data['move']==1) {
            if ($data['player']) $char = 'o';
            else $char = 'x';

            $data['table'][$data['last'][0]][$data['last'][1]] = $char;
            $data['move']=2;
        } else {
            if($data['player']) $char = 'x';
            else $char = 'o';

             $data['table'][$data['last'][0]][$data['last'][1]] = $char;
            $data['move']=1;
        }

        array_push($data['board'], $data['last']);

        file_put_contents($filename, json_encode($data));
        echo json_encode($data);

        return;
    }

    if(isset($_GET['move']) && isset($_GET['check']) && isset($_GET['code'])){
        $filename = "./".$_GET['code'].".json";
        $data = json_decode(file_get_contents($filename),true);

        if(($data['table'][0][0]==$table['table'][0][1]) && ($data['table'][0][1]==$data['table'][0][2])) $data['win']=$data['table'][0][0];
        else if (($data['table'][1][0]==$table['table'][1][1]) && ($data['table'][1][1]==$data['table'][1][2])) $data['win']=$data['table'][1][0];
        else if (($data['table'][2][0]==$table['table'][2][1]) &&($data['table'][2][1]==$data['table'][2][2])) $data['win'] = $data['table'][2][0];
        else if (($data['table'][0][0]==$table['table'][1][0]) &&($data['table'][1][0]==$data['table'][2][0])) $data['win'] = $data['table'][0][0];
        else if (($data['table'][1][0]==$table['table'][1][1]) &&($data['table'][1][1]==$data['table'][1][2])) $data['win'] = $data['table'][1][0];
        else if (($data['table'][2][0]==$table['table'][2][1]) &&($data['table'][2][1]==$data['table'][2][2])) $data['win'] = $data['table'][2][0];
        else if (($data['table'][0][0]==$table['table'][1][1]) &&($data['table'][1][1]==$data['table'][2][2])) $data['win'] = $data['table'][0][0];
        else if (($data['table'][0][2]==$table['table'][1][1]) &&($data['table'][1][1]==$data['table'][2][0])) $data['win'] = $table['table'][1][1];
        else $data['win'] = null;

        echo json_encode($data);

        return;
    }

?>
