function createTriangular(elemnt,backColor,fillColor)
{
	var svgToHtmlText = "";
	svgToHtmlText += '<svg style="background-color:'+backColor+';" preserveAspectRatio="none" viewBox="-5 -5 110 110">';
	svgToHtmlText += '<title>polygon vector image</title>';
	svgToHtmlText += '<polygon points="50,1 100,100 1,100" fill="'+fillColor+'"/>';
	svgToHtmlText += '</svg>';
	elemnt.innerHTML = elemnt.innerHTML + svgToHtmlText;
}
function createCircle(elemnt,backColor,fillColor)
{
	var svgToHtmlText = "";
	svgToHtmlText += '<svg style="background-color:'+backColor+';" preserveAspectRatio="none" viewBox="-5 -5 110 110">';
	svgToHtmlText += '<title>Circle vector image</title>';
	svgToHtmlText += '<circle cx="50" cy="50" r="50" fill="'+fillColor+'"/>';
	svgToHtmlText += '</svg>';
	elemnt.innerHTML = elemnt.innerHTML + svgToHtmlText;
}

function createRectangle(elemnt,backColor,fillColor)
{
	var svgToHtmlText = "";
	svgToHtmlText += '<svg style="background-color:'+backColor+';" preserveAspectRatio="none" viewBox="-5 -5 110 110">';
	svgToHtmlText += '<title>Rectangle vector image</title>';
	svgToHtmlText += '<polygon points="0,0 100,0 100,100 0,100" fill="'+fillColor+'"/>';
	svgToHtmlText += '</svg>';
	elemnt.innerHTML = elemnt.innerHTML + svgToHtmlText;
}

function createHexagonal(elemnt,backColor,fillColor)
{
	var svgToHtmlText = "";
	svgToHtmlText += '<svg style="background-color:'+backColor+';" preserveAspectRatio="none" viewBox="-5 -5 110 110">';
	svgToHtmlText += '<title>Rectangle vector image</title>';
	svgToHtmlText += '<polygon points="0,50 25,0 75,0 100,50 75,100 25,100" fill="'+fillColor+'"/>';
	svgToHtmlText += '</svg>';
	elemnt.innerHTML = elemnt.innerHTML + svgToHtmlText;
}